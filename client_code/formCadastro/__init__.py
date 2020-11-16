from ._anvil_designer import formCadastroTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class formCadastro(formCadastroTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)    
    self.drop_down_perfilusuario.items = [("Administrador", 1), ("Funcionário",2)]
    # Any code you write here will run when the form opens.

  def button_cancelar_click(self, **event_args):
    self.raise_event('x-close-alert')

  def button_criarconta_click(self, **event_args):
    nome = self.text_box_nomecompleto.text
    perfil = self.drop_down_perfilusuario.selected_value
    cpf = self.text_box_cpf.text
    email = self.text_box_email.text
    senha = self.text_box_senha.text
    verify_list = [nome, perfil, cpf, email, senha]
    for cat in verify_list:
      if cat == "":
        n = Notification("Por favor preencha todos os campos!")
        n.show()
        return    
    
    created = anvil.server.call("inserir_usuario", nome, perfil, cpf, email, senha)
    if created :
      n=Notification("Conta criada. Aguarde o administrador liberar seu acesso")
      n.show()
      open_form('homepageComum')
    
      
  def checaConfSenha(self, **event_args):
    print(self.text_box_confirmasenha.text)
    print(self.text_box_senha.text)
    senhas_iguais = (self.text_box_senha.text == self.text_box_confirmasenha.text)
    if not senhas_iguais:
      self.label_senhas_diferentes.visible = True
      return False
    if self.text_box_confirmasenha == "" or self.text_box_senha == "":
      self.label_senhas_diferentes.visible = False
      return False        
    return True
  



