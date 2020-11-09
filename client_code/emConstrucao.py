from ._anvil_designer import emConstrucaoTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .homepageAdm.ambiente_popup import ambiente_popup

class emConstrucao(emConstrucaoTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.user = ""
    self.init_components(**properties)
    
    # Any code you write here will run when the form opens.    
    



 


