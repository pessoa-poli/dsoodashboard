from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):    
    # Set Form properties and Data Bindings.    
    self.init_components(**properties)
    print(self.item)
    self.drop_down_perfil.items = {("Administrador","1"), ("Funcionário","2")} 
    if self.item['cadastroConfirmado']:
      self.button_statusconta.icon = "_/theme/controls-green.png"
      self.button_statusconta.text = "ativo"
      self.button_statusconta.tag = True
    if not self.item['cadastroConfirmado']:
      self.button_statusconta.tag = False

    # Any code you write here will run when the form opens.

    

  def drop_down_perfil_change(self, **event_args):
    print(f"Selected value is {self.drop_down_perfil.selected_value}")    
    pasa = anvil.server.call('modificar_perfil_usuario',
                      novoPerfilUsuario=self.drop_down_perfil.selected_value ,
                      idUsuario=self.item['id'])
    print(pasa)
    
  def button_statusconta_click(self, **event_args):
    if self.button_statusconta.tag:
      self.button_statusconta.icon = "_/theme/controls-red.png"
      self.button_statusconta.text = "inativo"
      self.button_statusconta.tag = False
      anvil.server.call("ativar_desativar_cadastro_usuario",
                        cadastroConfirmado=self.button_statusconta.tag,
                        idUsuario=self.item['id'])
      return
    if not self.button_statusconta.tag:
      self.button_statusconta.icon = "_/theme/controls-green.png"
      self.button_statusconta.text = "ativo"
      self.button_statusconta.tag = True
      anvil.server.call("ativar_desativar_cadastro_usuario",
                        cadastroConfirmado=self.button_statusconta.tag,
                        idUsuario=self.item['id'])
      return





