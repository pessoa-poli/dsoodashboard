import anvil.server
import hashlib

def lembrar_do_usuario():
	if "lembrardemim" in anvil.server.cookies.local and anvil.server.cookies.local["lembrardemim"]:
		user = return_current_user()
		return user
	else:
		return False

def get_email_do_cookie():	
	return anvil.server.cookies.local.get("email", "")
	

def login(conn, email, senha, lembrardemim):
	anvil.server.cookies.local["email"] = email
	anvil.server.cookies.local['lembrardemim'] = lembrardemim
	hashSenha = hashlib.md5(senha.encode('utf-8')).hexdigest()
	with conn.cursor() as cur:
		query = """SELECT * FROM usuario u
					WHERE u.email = %(email)s AND u.senha = %(senha)s"""
		params = {'email': email, 'senha': hashSenha}

		cur.execute(query, params)
		myUser = cur.fetchall()
		if len(myUser) == 1:
			  anvil.server.cookies.local["user"] = myUser[0]
		foundUser = (len(myUser) == 1)
		return foundUser

def logout():
	anvil.server.cookies.local["user"] = {}

def return_current_user():
	currentUser = anvil.server.cookies.local["user"]
	userSafeToReturnDict = {"id":currentUser['id'], "nome":currentUser['nome'],
	"perfilUsuario":currentUser['perfilUsuario'], "cadastroConfirmado":currentUser['cadastroConfirmado'], "cpf":currentUser['cpf'], "email":currentUser['email']}
	return userSafeToReturnDict