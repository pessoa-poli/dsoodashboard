from ._anvil_designer import loginLightboxTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..formCadastro import formCadastro
import time

class loginLightbox(loginLightboxTemplate):
  def __init__(self, **properties):    
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.text_box_email.text = anvil.server.call('get_email_do_cookie')
    #if self.usuario_lembrado:
      #self.text_box_email.text = self.usuario_lembrado['email']

    # Any code you write here will run when the form opens.

  def button_login_click(self, **event_args):
    lembrarusuario = self.check_box_lembrardemim.checked    
    found_me = anvil.server.call('login', email=self.text_box_email.text, senha=self.text_box_senha.text, lembrardemim=lembrarusuario)
    if found_me:
      usuario_logado = anvil.server.call("return_current_user")
      if usuario_logado['perfilUsuario'] == 1:
        self.raise_event('x-close-alert')
        open_form('homepageAdm')
      if usuario_logado['perfilUsuario'] == 2:
        self.raise_event('x-close-alert')
        open_form('homepageLimpeza')
      n = Notification("Bem vindo ao Dashboard!")
      n.show()      
    if not found_me:     
      n = Notification("Usuario ou senha incorretos")
      n.show()     
      
    

  def link_cadastrese_click(self, **event_args):
    self.raise_event('x-close-alert')
    alert(content=formCadastro(), buttons=[],dismissible=True,large=True,title="Faça seu cadastro.")
    

