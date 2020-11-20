from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run when the form opens.
    self.check_status()
    print(self.item)
  def check_status(self, **event_args):
    if self.item['co2'] >= 700:
      self.image_co2.source = "_/theme/co2-critico.png"
    '''if self.item['capacidade_de_pessoas_ultrapassada']:
      self.image_capacity.source = "_/theme/overcapacity.png"'''
  