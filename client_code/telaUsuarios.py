from ._anvil_designer import telaUsuariosTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .homepageAdm.ambiente_popup import ambiente_popup
from .homepageLimpeza import homepageLimpeza

class telaUsuarios(telaUsuariosTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.user = ""
    self.init_components(**properties)
    self.repeating_panel_usuarios.items = [{'nome':'Marcelo'},{'nome':'Marcelo'},{'nome':'Natália'},{'nome':'Jonas'},{'nome':'Maria'},]
    # Any code you write here will run when the form opens. 

  def visao_geral_link_click(self, **event_args):
    open_form('homepageAdm')

  def link_limpezamanutencao_click(self, **event_args):
    open_form('homepageLimpeza')





 


