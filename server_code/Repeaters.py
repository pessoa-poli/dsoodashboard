from datetime import datetime, timedelta

def get_lista_salas(conn):
	with conn.cursor() as cur:
		cur.execute("""SELECT i.*,
						CAST(dioxido.valor AS INTEGER) as co2,
						CAST(pessoa.valor AS INTEGER) as "qtdPessoas",
						(pessoa.valor > i."capacidadePessoas") as "capacidadeUltrapassada"
					FROM instalacao i
						JOIN medicao pessoa on pessoa."idInstalacao" = i.id
						JOIN medicao dioxido on dioxido."idInstalacao" = i.id
					WHERE dioxido."tipoDado" = 'CO2' AND dioxido."ultimaMedicao" = TRUE
						AND pessoa."tipoDado" = 'Pessoas' AND pessoa."ultimaMedicao" = TRUE""")

		ret = cur.fetchall()
		return ret

def get_sala_pelo_nome(conn, nome_sala):  
	with conn.cursor() as cur:
		query = """SELECT i."necessitaLimpeza",
					i."necessitaManutencao", nR."nomeNivel",
					CAST(dioxido.valor AS INTEGER) as co2,
					CAST(pessoa.valor AS INTEGER) as "qtdPessoas",
					(pessoa.valor > i."capacidadePessoas") as "capacidadeUltrapassada"
				FROM instalacao i
					JOIN medicao pessoa on pessoa."idInstalacao" = i.id
					JOIN medicao dioxido on dioxido."idInstalacao" = i.id
					JOIN "nivelRisco" nR on nR.id = i."nivelRisco"
				WHERE dioxido."tipoDado" = 'CO2' AND dioxido."ultimaMedicao" = TRUE
					AND pessoa."tipoDado" = 'Pessoas' AND pessoa."ultimaMedicao" = TRUE
					AND i.nome = %(nome)s
				ORDER BY i.id"""
		
		params = {'nome': nome_sala}

		cur.execute(query, params)
		ret = cur.fetchall()

	return {
		'co2': int(ret[0]['co2']),
		'qtdPessoas': int(ret[0]['qtdPessoas']),
		'capacidadeUltrapassada': ret[0]['capacidadeUltrapassada'],
		'necessitaManutencao': ret[0]['necessitaManutencao'],
		'necessitaLimpeza': ret[0]['necessitaLimpeza'],
		'nivel_risco': ret[0]['nomeNivel']
	}

def busca_crises_atribuidas_ao_usuario(cur, idUsuario):
	query = """SELECT DISTINCT ON (n."tipoNotificacao", n."idInstalacao")
				u.nome AS "nomeUsuario", n.id AS "idNotificacao", i.nome AS "nomeInstalacao", tn.nome AS "tipoNotificacao", n."dataUltimaAlteracao"
			FROM notificacao n
				JOIN instalacao i ON n."idInstalacao" = i.id
				JOIN usuario u ON n."idUsuarioResponsavel" = u.id
				JOIN "tipoNotificacao" tn ON n."tipoNotificacao" = tn.id
			WHERE n.resolvida = FALSE AND (i."necessitaLimpeza" = TRUE OR i."necessitaManutencao" = TRUE)
				AND n."idUsuarioResponsavel" = %(idUsuario)s
			ORDER BY n."tipoNotificacao", n."idInstalacao", u.nome, n.id;"""

	params = {'idUsuario': idUsuario}

	cur.execute(query, params)
	return cur.fetchall()

def busca_crises_nao_artibuidas_ao_usuario(cur, idUsuario):
	query = """SELECT DISTINCT ON (n."tipoNotificacao", n."idInstalacao")
				u.nome AS "nomeUsuario", n.id AS "idNotificacao", i.nome AS "nomeInstalacao", tn.nome AS "tipoNotificacao", n."dataUltimaAlteracao"
			FROM notificacao n
				JOIN instalacao i ON n."idInstalacao" = i.id
				LEFT JOIN usuario u ON n."idUsuarioResponsavel" = u.id
				JOIN "tipoNotificacao" tn ON n."tipoNotificacao" = tn.id
			WHERE n.resolvida = FALSE AND (i."necessitaLimpeza" = TRUE OR i."necessitaManutencao" = TRUE)
			ORDER BY n."tipoNotificacao", n."idInstalacao", u.nome, n.id;"""

	cur.execute(query)
	return cur.fetchall()

def busca_crises(conn, idUsuario):	
	with conn.cursor() as cur:
		crisesUsuario = busca_crises_atribuidas_ao_usuario(cur, idUsuario)
		if crisesUsuario:
			result = list(filter(
				lambda crise: (datetime.utcnow() - crise['dataUltimaAlteracao'] < timedelta(minutes=3)), crisesUsuario
			))
			return result

		crisesNaoUsuario = busca_crises_nao_artibuidas_ao_usuario(cur, idUsuario)
		if crisesNaoUsuario:
			result = list(filter(
				lambda crise: crise['nomeUsuario'] == None or (datetime.utcnow() - crise['dataUltimaAlteracao'] < timedelta(minutes=3)), crisesNaoUsuario
			))
			return result


def busca_novas_crises(conn, idUsuario, listaCrisesVelha):
	crisesNaBase = busca_crises(conn, idUsuario)
	if crisesNaBase == None:
		crisesNaBase = []
	novasCrises = [cat for cat in crisesNaBase if cat not in listaCrisesVelha]
	if len(novasCrises) > 0 :
		return crisesNaBase
	return []
	
	