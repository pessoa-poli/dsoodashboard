import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import threading
import psycopg2
import psycopg2.extras
from TipoNotificacao import TipoNotificacao
import Usuario as user
import QuadrosInformacao as qi
import Login as log
import Repeaters as rep
import Responsabilidade as resp
import Crise as crise

anvil.server.connect("QDYIJLYLCRW762NRFKH6Z3EY-B4CFZ34JETACVQWU")

lock = threading.Lock()
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

conn = connect()

@anvil.server.callable
def buscar_instalacoes_responsabilizadas_limpeza(idUsuario):
	return  resp.buscar_instalacoes_responsabilizadas_limpeza(conn, idUsuario)

@anvil.server.callable
def buscar_instalacoes_responsabilizadas(idUsuario):
	return resp.buscar_instalacoes_responsabilizadas(conn, idUsuario)

@anvil.server.callable
def buscar_responsavel_limpeza(nome_sala):
	return resp.buscar_responsavel_limpeza(conn, nome_sala)
	
@anvil.server.callable
def buscar_responsavel_manutencao(nome_sala):
	return resp.buscar_responsavel_manutencao(conn, nome_sala)

# return: lista de RealDictRow
@anvil.server.callable
def get_total_salas():
	return qi.get_total_salas(conn)

# return: lista de RealDictRow
@anvil.server.callable
def get_lista_salas():
	return rep.get_lista_salas(conn)

# return: quantidade de salas com risco baixo
@anvil.server.callable
def get_count_salas_baixo_risco():
	return qi.get_count_salas_baixo_risco(conn)

# return: quantidade de salas com risco medio
@anvil.server.callable
def get_count_salas_medio_risco():
	return qi.get_count_salas_medio_risco(conn)

# return: quantidade de salas com risco alto
@anvil.server.callable
def get_count_salas_alto_risco():
	return qi.get_count_salas_alto_risco(conn)

# return: número de pessoas nas instalações, float
@anvil.server.callable
def get_count_usuarios_presentes():
	return qi.get_count_usuarios_presentes(conn)

# return: float
@anvil.server.callable
def get_count_salas_disponiveis_pra_uso():
	return qi.get_count_salas_disponiveis_pra_uso(conn)

@anvil.server.callable
def get_count_salas_indisponiveis_para_uso():
	return qi.get_count_salas_alto_risco(conn)

# id_sala: int
# return: lista de RealDictRow
@anvil.server.callable
def get_sala_pelo_id(id_sala):
	with conn.cursor() as cur:
		query = """SELECT * FROM instalacao i
				WHERE i.id = %(id)s"""
		params = {'id': id_sala}

		cur.execute(query, params)
		return cur.fetchall()

@anvil.server.callable
def get_sala_pelo_nome(nome_sala):  
	return rep.get_sala_pelo_nome(conn, nome_sala)

@anvil.server.callable
def lembrar_do_usuario():
	return log.lembrar_do_usuario()

@anvil.server.callable
def get_email_do_cookie():
	return log.get_email_do_cookie()

@anvil.server.callable
def login(email, senha, lembrardemim):
	return log.login(conn, email, senha, lembrardemim)

@anvil.server.callable
def logout():
	return log.logout()

@anvil.server.callable		
def return_current_user():
	return log.return_current_user()

# mostra crises sem responsável/que foram atribuídas a algum usuário há 3 minutos.
@anvil.server.callable
def busca_crises(idUsuario):
	return rep.busca_crises(conn, idUsuario)

@anvil.server.callable
def atribuir_usuario_a_crise(idUsuario, idNotificacao):
	lock.acquire()
	ret = crise.atribuir_usuario_a_crise(conn, idUsuario, idNotificacao)
	lock.release()
	return ret

@anvil.server.callable
def marca_sala_para_limpeza(id_sala):
	return crise.marca_sala_para_limpeza(conn, id_sala)

@anvil.server.callable
def marca_sala_para_manutencao(id_sala):
	return crise.marca_sala_para_manutencao(conn, id_sala)

@anvil.server.callable
def resolve_crise_limpeza(idInstalacao):
	return crise.resolve_crise_limpeza(conn, idInstalacao)

@anvil.server.callable
def resolve_crise_manutencao(idInstalacao):
	return crise.resolve_crise_manutencao(conn, idInstalacao)

@anvil.server.callable
def busca_usuarios():
	return user.busca_usuarios(conn)

@anvil.server.callable
def inserir_usuario(nome, perfil, cpf, email, senha):
	return user.inserir_usuario(conn, nome, perfil, cpf, email, senha)

# cadastroConfirmado: boolean
# idUsuario: number
@anvil.server.callable
def ativar_desativar_cadastro_usuario(cadastroConfirmado, idUsuario):
	return user.ativar_desativar_cadastro_usuario(conn, cadastroConfirmado, idUsuario)

# novoPerfilUsuario: number
# idUsuario: number
@anvil.server.callable
def modificar_perfil_usuario(novoPerfilUsuario, idUsuario):
	return user.modificar_perfil_usuario(conn, novoPerfilUsuario, idUsuario)

@anvil.server.callable
def busca_novas_crises(idUsuario, listaCrisesVelha):
	return rep.busca_novas_crises(conn, idUsuario, listaCrisesVelha)

anvil.server.wait_forever()