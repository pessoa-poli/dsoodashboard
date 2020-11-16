from ._anvil_designer import warningsTemplateTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class warningsTemplate(warningsTemplateTemplate):
  def __init__(self, **properties):
    self.usuario_logado = anvil.server.call('return_current_user')
    # Set Form properties and Data Bindings.    
    self.init_components(**properties)
    self.showRightDiv()
    # Any code you write here will run when the form opens.    
    
  def showRightDiv(self):
    print(self.item)
    if self.item['nomeUsuario'] is None:
      self.flow_panel_vermelho.visible =  True
      self.flow_panel_amarelo.visible = False
      return    
    self.flow_panel_vermelho.visible =  False
    self.flow_panel_amarelo.visible = True
      

  def button_assumiressecaso_click(self, **event_args):
    worked = anvil.server.call("atribuir_usuario_a_crise", idUsuario=self.usuario_logado['id'], idInstalacao=self.item['idInstalacao'])
    if worked:
      n=Notification("Caso assumido!")
      n.show()



