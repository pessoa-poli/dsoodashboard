from ._anvil_designer import limpeza_repeater_templateTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class limpeza_repeater_template(limpeza_repeater_templateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run when the form opens.
    

  def button_marcar_limpa_click(self, **event_args):
    anvil.server.call('resolve_crise', self.item['id'], 'Limpeza')
    self.parent.raise_event('x-refresh-panels')

  def button_necessita_limpeza_click(self, **event_args):
    anvil.server.call('marca_sala_para_limpeza', self.item['id'])


