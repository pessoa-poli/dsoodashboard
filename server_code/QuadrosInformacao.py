import Risco as risco

def get_total_salas(conn):
	with conn.cursor() as cur:
		cur.execute("SELECT count(*) FROM instalacao")
		return cur.fetchone()['count']

def get_count_usuarios_presentes(conn):
	with conn.cursor() as cur:
		cur.execute("""SELECT CAST(SUM(valor) as INTEGER) as sum FROM medicao
					WHERE "tipoDado" = 'Pessoas'
						AND "ultimaMedicao" = TRUE""")
		return cur.fetchone()['sum']

def get_count_salas_baixo_risco(conn):
	return risco.get_count_salas_baixo_risco(conn)

def get_count_salas_medio_risco(conn):
	return risco.get_count_salas_medio_risco(conn)

def get_count_salas_alto_risco(conn):
	return risco.get_count_salas_alto_risco(conn)

def get_count_salas_disponiveis_pra_uso(conn):
	return risco.get_count_salas_disponiveis_pra_uso(conn)