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
    if self.item['nomeUsuario'] == "none":
      self.data_row_panel_semresponsavel.visible = False
      self.data_row_panel_semcrisesnomomento.visible = True
      return
    if self.item['nomeUsuario'] is not None:
      self.label_amarela_tipoproblema.text = f"Sala {self.item['nomeInstalacao']} possui problemas de {self.item['tipoNotificacao']}."
      self.button_assumiressecaso.text = f"O usuario {self.item['nomeUsuario']} já está tomando providências."
      self.button_assumiressecaso.visible = False
      self.label_usuarioresponsabel.visible = True
      self.data_row_panel_semresponsavel.role = "warningyellow"
     
      #self.flow_panel_vermelho.visible =  True
      #self.flow_panel_amarelo.visible = False
      #return    
    #self.flow_panel_vermelho.visible =  False
    #self.flow_panel_amarelo.visible = True
      

  def button_assumiressecaso_click(self, **event_args):    
    worked = anvil.server.call("atribuir_usuario_a_crise", idUsuario=self.usuario_logado['id'], idNotificacao=self.item['idNotificacao'])
    if worked:
      n=Notification("Caso assumido!")
      n.show()



