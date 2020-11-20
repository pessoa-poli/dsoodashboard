from TipoNotificacao import TipoNotificacao

# nome_sala: string
# limpeza: boolean
# return: lista de RealDictRow
def buscar_responsavel(conn, nome_sala, crise):
	with conn.cursor() as cur:
		query = """SELECT u.* FROM usuario u
					JOIN notificacao n ON n."idUsuarioResponsavel" = u.id
					JOIN instalacao i ON n."idInstalacao" = i.id
				WHERE i.nome = %(nomeInstalacao)s"""

		where = ""
		if crise is TipoNotificacao.Limpeza:
			where = " AND i.\"necessitaLimpeza\" = TRUE"
		elif crise is TipoNotificacao.Manutencao:
			where = " AND i.\"necessitaManutencao\" = TRUE"
		else: return

		params = {'nomeInstalacao': nome_sala}

		cur.execute(query + where, params)
		return cur.fetchall()

def buscar_responsavel_limpeza(conn, nome_sala):
	return buscar_responsavel(conn, nome_sala, TipoNotificacao.Limpeza)
	
def buscar_responsavel_manutencao(conn, nome_sala):
	return buscar_responsavel(conn, nome_sala, TipoNotificacao.Manutencao)

def buscar_instalacoes_responsabilizadas_limpeza(conn, idUsuario):
	with conn.cursor() as cur:
		query = """SELECT DISTINCT ON (i.id) i.id, i.nome FROM instalacao i
					JOIN notificacao n ON i.id = n."idInstalacao"
					LEFT JOIN usuario u ON n."idUsuarioResponsavel" = u.id
				WHERE n.resolvida = FALSE AND u.id = %(idUsuario)s
					AND i."necessitaLimpeza" = TRUE
				ORDER BY i.id ASC, n.id DESC"""
		params = {'idUsuario': idUsuario}
		cur.execute(query, params)

		return cur.fetchall()

def buscar_instalacoes_responsabilizadas(conn, idUsuario):
	with conn.cursor() as cur:
		query = """SELECT DISTINCT ON (i.id) i.id, i.nome, i."necessitaLimpeza", i."necessitaManutencao" FROM instalacao i
					JOIN notificacao n on i.id = n."idInstalacao"
					JOIN usuario u on n."idUsuarioResponsavel" = u.id
				WHERE u.id = %(idUsuario)s
				ORDER BY i.id asc, n.id desc"""
		params = {'idUsuario': idUsuario}
		cur.execute(query, params)

		return cur.fetchall()