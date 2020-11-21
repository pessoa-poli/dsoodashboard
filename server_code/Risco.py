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
def get_ultimas_medicoes(conn, nome_instalacao=""):
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
def get_count_salas_risco_all(conn):
	risco = {'baixo': 0, 'medio': 0, 'alto': 0}
	ultimasMedicoes = get_ultimas_medicoes(conn)
	for medicao in ultimasMedicoes.values():
		risco[calcula_risco(medicao)] += 1
	
	return risco

# risco: string, pode ser 'baixo', 'medio' ou 'alto'
# return: quantidade de salas com o risco especificado
def get_count_salas_risco(conn, risco):
	qtdSalasRisco = 0
	ultimasMedicoes = get_ultimas_medicoes(conn)
	for medicao in ultimasMedicoes.values():
		if calcula_risco(medicao) == risco:
			qtdSalasRisco += 1
	
	return qtdSalasRisco

# return: quantidade de salas com risco baixo
def get_count_salas_baixo_risco(conn):
	return get_count_salas_risco(conn, 'baixo')

# return: quantidade de salas com risco medio
def get_count_salas_medio_risco(conn):
	return get_count_salas_risco(conn, 'medio')

# return: quantidade de salas com risco alto
def get_count_salas_alto_risco(conn):
	return get_count_salas_risco(conn, 'alto')

def get_count_salas_disponiveis_pra_uso(conn):
	riscoDict = get_count_salas_risco_all(conn)
	return riscoDict['baixo'] + riscoDict['medio']