from TipoNotificacao import TipoNotificacao

def atribuir_usuario_a_crise(conn, idUsuario, idNotificacao):
	with conn.cursor() as cur:
		query = """UPDATE notificacao
					SET "idUsuarioResponsavel" = %(idUsuario)s,
						"dataUltimaAlteracao" = NOW()
					WHERE id = %(idNotificacao)s AND "idUsuarioResponsavel" IS NULL"""
		params = {'idUsuario': idUsuario, 'idNotificacao': idNotificacao}

		cur.execute(query, params)
		conn.commit()
		ret = cur.rowcount > 0
	return ret

def marca_crise_para_sala(conn, id_sala, crise):
	with conn.cursor() as cur:
		update = "UPDATE instalacao"

		querySet = ""
		if crise is TipoNotificacao.Limpeza:
			querySet = " SET i.\"necessitaLimpeza\" = TRUE"
		elif crise is TipoNotificacao.Manutencao:
			querySet = " SET i.\"necessitaManutencao\" = TRUE"
		else: return

		where = " WHERE id = %(id)s"

		query = update + querySet + where
		params = {'id': id_sala}

		cur.execute(query, params)
		conn.commit()
		if cur.rowcount > 0: return insere_notificacao(id_sala, crise)
		else: return False

def insere_notificacao(conn, id_sala, crise):
	tipo = crise.value
	with conn.cursor() as cur:
		query = """INSERT INTO notificacao ("tipoNotificacao", "idInstalacao", "idUsuarioResponsavel", "dataNotificacao", "dataUltimaAlteracao")
					VALUES (%(tipo)s, %(idInstalacao)s, null, now(), now())"""
		params = {
			'tipo': tipo,
			'idInstalacao': id_sala
		}

		cur.execute(query, params)
		conn.commit()
		return cur.rowcount > 0

def deleta_notificacoes_repetidas(cur, idInstalacao, tipo):
	query = """DELETE FROM notificacao
					WHERE resolvida = FALSE
						AND "idUsuarioResponsavel" IS NULL
						AND "idInstalacao" = %(idInstalacao)s
						AND "tipoNotificacao" = %(tipo)s"""
	params = {'idInstalacao': idInstalacao, "tipo": tipo}
	cur.execute(query, params)
	return cur.rowcount > 0

def atualiza_instalacao(cur, idInstalacao, crise):
	query = "UPDATE instalacao"

	querySet = ""
	if crise is TipoNotificacao.Limpeza:
		querySet = " SET \"necessitaLimpeza\" = FALSE"
	elif crise is TipoNotificacao.Manutencao:
		querySet = " SET \"necessitaManutencao\" = FALSE"
	else: return
	
	where = " WHERE id = %(idInstalacao)s"

	query += querySet + where
	params = {'idInstalacao': idInstalacao}

	cur.execute(query, params)
	return cur.rowcount > 0

def resolve_notificacao(cur, idInstalacao, tipo):
	query = """UPDATE notificacao
				SET resolvida = TRUE,
					"dataUltimaAlteracao" = NOW()
				WHERE resolvida = FALSE
					AND "tipoNotificacao" = %(tipo)s
					AND "idInstalacao" = %(idInstalacao)s"""
	params = {"tipo": tipo, "idInstalacao": idInstalacao}

	cur.execute(query, params)
	return cur.rowcount > 0

def resolve_crise(conn, idInstalacao, crise):
	with conn.cursor() as cur:
		tipo = crise.value
		if not deleta_notificacoes_repetidas(cur, idInstalacao, tipo):
			cur.rollback()
			return
		
		if not atualiza_instalacao(cur, idInstalacao, crise):
			cur.rollback()
			return

		if not resolve_notificacao(cur, idInstalacao, tipo):
			cur.rollback()
			return

		conn.commit()

def resolve_crise_limpeza(conn, idInstalacao):
	return resolve_crise(conn, idInstalacao, TipoNotificacao.Limpeza)

def resolve_crise_manutencao(conn, idInstalacao):
	return resolve_crise(conn, idInstalacao, TipoNotificacao.Manutencao)

def marca_sala_para_limpeza(conn, id_sala):
	return marca_crise_para_sala(conn, id_sala, TipoNotificacao.Limpeza)

def marca_sala_para_manutencao(conn, id_sala):
	return marca_crise_para_sala(conn, id_sala, TipoNotificacao.Manutencao)