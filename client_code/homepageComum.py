from ._anvil_designer import homepageComumTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .homepageAdm.ambiente_popup import ambiente_popup

class homepageComum(homepageComumTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.user = ""
    self.init_components(**properties)
    
    # Any code you write here will run when the form opens.    
    self.dropdown_andar.items = ["1º Andar", "2º Andar", "3º Andar"]
    self.dropdown_andar.selected_value = self.dropdown_andar.items[0]
    self.dropdown_bloco.items = ["Bloco A","Bloco B","Bloco C","Bloco D","Bloco E","Bloco F","Bloco G","Bloco H",]
    self.dropdown_bloco.selected_value = self.dropdown_bloco.items[7]
    self.hide_markers()
    self.setup_FloorPlan_Markers("h111")
    self.dic_login = {'email':"", "senha":"", "lembrar_de_mim":False}
    
  def h111_marker_mouse_down(self, x, y, button, **event_args):
    responsavel = anvil.server.call('buscar_responsavel', meuid='h111')    
    myvar = alert(content=ambiente_popup(responsavel=responsavel),
               large=True,
               buttons=[],
               dismissible=True)

  def button_login_click(self, **event_args):
    self.user = anvil.users.login_with_form(show_signup_option=True, allow_remembered=True, allow_cancel=True)
    if self.user['nivel_acesso']['nome'] == "administrador":
      open_form('homepageAdm')
    if self.user['nivel_acesso']['nome'] == "limpeza":
      open_form('homepageLimpeza')
      
  def hide_markers(self, **event_args):
    self.h111_co2_image.visible = False    
    self.h111_overcapacity_image.visible = False         
    self.h111_maintenance_image.visible = False   
    self.h111_broom_image.visible = False    
    self.h111_green_marker.visible = False    
    self.h111_red_marker.visible = False   
    self.h111_yellow_marker.visible = False   
    self.h111_ok_image.visible = False

  def setup_FloorPlan_Markers(self, room, **event_args):
    sala = anvil.server.call('get_sala_pelo_id', id_sala="h111")
    critico = False
    if sala['co2_critico']:
      self.h111_co2_image.visible = True
      critico = True
    if sala['capacidade_de_pessoas_ultrapassada']:
      self.h111_overcapacity_image.visible = True
      critico = True
    if sala['precisa_manutencao']:      
      self.h111_maintenance_image.visible = True
      critico = True
    if sala['precisa_limpeza']:
      self.h111_broom_image.visible = True
      critico = True
    if sala['nivel_risco']['risco'] == "verde":
      self.h111_green_marker.visible = True      
    if sala['nivel_risco']['risco'] == "vermelho":
      self.h111_red_marker.visible = True      
    if sala['nivel_risco']['risco'] == "amarelo":
      self.h111_yellow_marker.visible = True    
    if not critico:
      self.h111_ok_image.visible = True

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    count = anvil.server.call('get_total_salas')
    pass





 


