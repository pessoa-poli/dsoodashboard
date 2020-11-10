import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import psycopg2
import psycopg2.extras

anvil.server.connect("JQ7UHKAJDDJ3252CEKTVVD3O-ZXFJGO77BAC3GJ6Q")


# Cada RealDictRow é um registro, e é um dicionário no qual:
	# Chave = nome da coluna
	# Valor = valor do registro na coluna especificada

# retorna uma conexão com um banco PostgreSQL
def connect():
	return psycopg2.connect(dbname='safeufrjdb',
		host='140.82.9.228',
		user='postgres',
		port='5432',
		password='postgres',
		cursor_factory=psycopg2.extras.RealDictCursor)

# nome_sala: string
# limpeza: boolean
# return: lista de RealDictRow
@anvil.server.callable
def buscar_responsavel(nome_sala, limpeza):
	conn = connect()
	with conn.cursor() as cur:
		query = """SELECT u.* FROM usuario u
					JOIN notificacao n ON n."idUsuarioResponsavel" = u.id
					JOIN instalacao i ON n."idInstalacao" = i.id"""
		
		where = " WHERE i.nome = %(nomeInstalacao)s"
		where += """ AND i."necessitaLimpeza" = TRUE""" if limpeza else """ AND i."necessitaManutencao" = TRUE"""
		cur.execute(query + where, {'nomeInstalacao': nome_sala})
		return cur.fetchall()

# return: lista de RealDictRow
@anvil.server.callable
def get_total_salas():
	conn = connect()
	with conn.cursor() as cur:
		cur.execute("SELECT count(*) FROM instalacao;")
		valores = cur.fetchall()
		if len(valores) > 0:
			return valores[0]
		else:
			return None

# return: lista de RealDictRow
@anvil.server.callable
def get_lista_salas():
	conn = connect()
	with conn.cursor() as cur:
		cur.execute("""SELECT i.*,
							CAST((select valor from medicao where "idInstalacao"=i.id and "ultimaMedicao"=TRUE and "tipoDado" = 'CO2') as INTEGER) as co2,
							CAST((select valor from medicao where "idInstalacao"=i.id and "ultimaMedicao"=TRUE and "tipoDado" = 'Pessoas') as INTEGER) as "qtdPessoas",
							CASE 
								WHEN (select valor from medicao where "idInstalacao"=i.id and "ultimaMedicao"=TRUE and "tipoDado" = 'Pessoas') > i."capacidadePessoas" THEN True
								ELSE False
							END as capacidadeUltrapassada
						FROM instalacao i""")
		ret = cur.fetchall()
		return(ret)

# valores_dict: dicionário com valores de:
	# 'capacidade': int
	# 'Pessoas': int
	# # 'CO2': float
	# 'Temperatura': float
	# 'Umidade': float
# return: nível de risco, 'baixo', 'medio', 'alto'.
def calcula_risco(valores_dict):
	co2 = valores_dict['CO2']
	pessoas = valores_dict['Pessoas']
	capacidade = valores_dict['capacidade']

	if co2 >= 1000: return 'alto'
	else:
		if pessoas > (2.0/3.0)*capacidade: return 'medio'
		else:
			if co2 > 400 and pessoas >= capacidade/2.0: return 'medio'
			else: return 'baixo'
		
# nome_instalacao: string
# return: dicionário com valores de:
	# 'capacidade': float
	# 'Pessoas': float
	# # 'CO2': float
	# 'Temperatura': float
	# 'Umidade': float
@anvil.server.callable
def get_ultimas_medicoes(nome_instalacao=""):
	conn = connect()
	with conn.cursor() as cur:
		query = """SELECT i.nome, m."tipoDado", m.valor, i."capacidadePessoas" FROM medicao m
					JOIN instalacao i ON m."idInstalacao" = i.id
				WHERE m."ultimaMedicao" = TRUE"""
		where = " AND i.nome = %(nome)s" if nome_instalacao else ""

		params = {'nome': nome_instalacao}
		cur.execute(query + where, params)
		dados = cur.fetchall()

	dadosDict = {}
	for dado in dados:
		agrupa_medidas_por_sala(dadosDict, dado['nome'], dado['capacidadePessoas'], dado['tipoDado'], dado['valor'])
	return dadosDict

# medidasSala: dicionário
# nome: nome da instalação, string
# capacidade: capacidade de cada instalação, int
# medida: tipo da medida, string
# valor: valor de cada medição, float
def agrupa_medidas_por_sala(medidasSala, nome, capacidade, medida, valor):
	if nome not in medidasSala:
		medidaDict = {'capacidade': capacidade}
		medidasSala[nome] = medidaDict
	medidasSala[nome][medida] = valor

# return: dicionário com a quantidade de cada tipo de risco encontrado no banco
def get_count_salas_risco_all():
	risco = {'baixo': 0, 'medio': 0, 'alto': 0}
	ultimasMedicoes = get_ultimas_medicoes()
	for medicao in ultimasMedicoes.values():
		risco[calcula_risco(medicao)] += 1
	
	return risco

# risco: string, pode ser 'baixo', 'medio' ou 'alto'
# return: quantidade de salas com o risco especificado
def get_count_salas_risco(risco):
	qtdSalasRisco = 0
	ultimasMedicoes = get_ultimas_medicoes()
	for medicao in ultimasMedicoes.values():
		if calcula_risco(medicao) == risco:
			qtdSalasRisco += 1
	
	return qtdSalasRisco

# return: quantidade de salas com risco baixo
@anvil.server.callable
def get_count_salas_baixo_risco():
	return get_count_salas_risco('baixo')

# return: quantidade de salas com risco medio
@anvil.server.callable
def get_count_salas_medio_risco():
	return get_count_salas_risco('medio')

# return: quantidade de salas com risco alto
@anvil.server.callable
def get_count_salas_alto_risco():
	return get_count_salas_risco('alto')

# return: número de pessoas nas instalações, float
@anvil.server.callable
def get_count_usuarios_presentes(): 
	conn = connect()
	with conn.cursor() as cur:
		cur.execute("""SELECT CAST(SUM(valor) as INTEGER) as sum FROM medicao
					WHERE "tipoDado" = 'Pessoas'
						AND "ultimaMedicao" = TRUE;""")
		return cur.fetchone()['sum']

# return: float
@anvil.server.callable
def get_count_salas_disponiveis_pra_uso():
	riscoDict = get_count_salas_risco_all()
	return riscoDict['baixo'] + riscoDict['medio']

# id_sala: int
# return: lista de RealDictRow
@anvil.server.callable
def get_sala_pelo_id(id_sala):   
	conn = connect()
	with conn.cursor() as cur:
		query = """SELECT * FROM instalacao i
				WHERE i.id = %(id)s"""
		params = {'id': id_sala}

		cur.execute(query, params)
		return cur.fetchall()

@anvil.server.callable
def get_sala_pelo_nome(nome_sala):  

	conn = connect()
	with conn.cursor() as cur:

		query = """SELECT i.nome, i."necessitaLimpeza", i."necessitaManutencao",
						(select valor from medicao where "idInstalacao"=i.id and "ultimaMedicao"=TRUE and "tipoDado" = 'CO2') as co2,
						CASE 
							WHEN (select valor from medicao where "idInstalacao"=i.id and "ultimaMedicao"=TRUE and "tipoDado" = 'Pessoas') > i."capacidadePessoas" THEN True
							ELSE False
						END as "capacidadeUltrapassada"
					FROM instalacao i
					WHERE i.nome = %(nome)s"""
		
		params = {'nome': nome_sala}

		cur.execute(query, params)
		ret = cur.fetchall()
		retTratado = {
			'co2': int(ret[0]['co2']),
			'capacidadeUltrapassada': ret[0]['capacidadeUltrapassada'],
			'necessitaManutencao': ret[0]['necessitaManutencao'],
			'necessitaLimpeza': ret[0]['necessitaLimpeza'],
			'nivel_risco': {
				'risco': 'verde'
			}
		}
		return retTratado

@anvil.server.callable
def atualiza_sala(salas_row, sala_dic):  
	if app_tables.salas.has_row(salas_row):
		salas_row.update(**sala_dic)
	else:
		raise Exception("A sala não existe mais.")


anvil.server.wait_forever()