from ._anvil_designer import dev_roomTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class dev_room(dev_roomTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run when the form opens.
    self.repeating_panel_1.items = anvil.server.call('get_lista_salas')

  def link_sair_click(self, **event_args):
    anvil.users.logout()
    open_form('homepageComum')

  def link_visao_geral_click(self, **event_args):
    open_form('homepageAdm')


