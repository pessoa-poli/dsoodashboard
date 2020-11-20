from ._anvil_designer import telaUsuariosTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .homepageAdm import homepageAdm
from .homepageLimpeza import homepageLimpeza

class telaUsuarios(telaUsuariosTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.user = ""
    self.init_components(**properties)
    self.repeating_panel_usuarios.items = anvil.server.call('busca_usuarios')
    
    # Any code you write here will run when the form opens. 

  def visao_geral_link_click(self, **event_args):
    open_form('homepageAdm')

  def link_limpezamanutencao_click(self, **event_args):
    open_form('homepageLimpeza')

  def link_1_click(self, **event_args):
    anvil.server.call('logout')
    open_form('homepageComum')
    n = Notification("Logout efetuado com sucesso")
    n.show()






 


