from ._anvil_designer import ambiente_popupTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ambiente_popup(ambiente_popupTemplate):
  def __init__(self, responsavel="Cláudio Esperança", **properties):
    self.responsavel = responsavel
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.responsavel_label.text = self.responsavel