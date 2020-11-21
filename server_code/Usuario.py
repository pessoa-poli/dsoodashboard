import hashlib
import multiprocessing
import time

def ativar_desativar_cadastro_usuario(conn, cadastroConfirmado, idUsuario):
	with conn.cursor() as cur:
		query = """UPDATE usuario
			        SET "cadastroConfirmado" = %(cadastroConfirmado)s
			        WHERE id = %(idUsuario)s;"""
		
		params = {'cadastroConfirmado': cadastroConfirmado, 'idUsuario': idUsuario}

		cur.execute(query, params)
		#return cur.fetchall()

def modificar_perfil_usuario(conn, novoPerfilUsuario, idUsuario):	
	with conn.cursor() as cur:
		query = """UPDATE usuario
			        SET "perfilUsuario" = %(novoPerfilUsuario)s
			        WHERE id = %(idUsuario)s;"""
		
		params = {'novoPerfilUsuario': novoPerfilUsuario, 'idUsuario': idUsuario}
		cur.execute(query, params)
		conn.commit()
	return "finished"

def busca_usuarios(conn):
	with conn.cursor() as cur:
		cur.execute("SELECT * FROM usuario")
		return cur.fetchall()

def inserir_usuario(conn, nome, perfil, cpf, email, senha):
	hashSenha = hashlib.md5(senha.encode('utf-8')).hexdigest()
	with conn.cursor() as cur:
		query = """INSERT INTO usuario (nome, "perfilUsuario", "cadastroConfirmado", cpf, email, senha)
					VALUES (%(nome)s, %(perfil)s, FALSE, %(cpf)s, %(email)s, %(senha)s)"""

		params = {
			'nome': nome,
			'perfil': perfil,
			'cpf': cpf,
			'email': email,
			'senha': hashSenha
		}

		cur.execute(query, params)
		conn.commit()
		return cur.rowcount > 0