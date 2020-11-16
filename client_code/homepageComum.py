from ._anvil_designer import homepageComumTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .homepageAdm.ambiente_popup import ambiente_popup
from .loginLightbox import loginLightbox

class homepageComum(homepageComumTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.user = ""
    self.dropdown_andar.items = ["1º Andar", "2º Andar", "3º Andar"]
    self.dropdown_andar.selected_value = self.dropdown_andar.items[0]
    self.dropdown_bloco.items = ["Bloco A","Bloco B","Bloco C","Bloco D","Bloco E","Bloco F","Bloco G","Bloco H",]
    self.dropdown_bloco.selected_value = self.dropdown_bloco.items[7]
    self.hide_markers()
    self.setup_FloorPlan_Markers("H-111")
    self.dic_login = {'email':"", "senha":"", "lembrar_de_mim":False}
    
    self.init_components(**properties)
    
    # Any code you write here will run when the form opens.    
    
    
  def h111_marker_mouse_down(self, x, y, button, **event_args):
    responsavel = anvil.server.call('buscar_responsavel', meuid='H-111')    
    myvar = alert(content=ambiente_popup(responsavel=responsavel),
               large=True,
               buttons=[],
               dismissible=True)

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
    sala = anvil.server.call('get_sala_pelo_nome', nome_sala="H-111")     
    self.h111_co2_image.visible = sala['co2'] > 1000
    self.h111_overcapacity_image.visible = sala['capacidadeUltrapassada']         
    self.h111_maintenance_image.visible = sala['necessitaManutencao']    
    self.h111_broom_image.visible = sala['necessitaLimpeza']      
    if sala['nivel_risco'] == "Baixo":
      self.h111_green_marker.visible = True
    if sala['nivel_risco'] == "Médio":
      self.h111_yellow_marker.visible = True  
    if sala['nivel_risco'] == "Elevado":
      self.h111_red_marker.visible = True    
    self.h111_ok_image.visible = not (sala['co2'] > 1000 or sala['capacidadeUltrapassada'] or sala['necessitaManutencao'] or sala['necessitaLimpeza'])


  def link_login_click(self, **event_args):
    alert(
      content=loginLightbox(),
      title="Faça seu login",
      large=True,
      dismissible=True,
    )

  def timer_1_tick(self, **event_args):
    with anvil.server.no_loading_indicator:
      self.setup_FloorPlan_Markers("H-111")
      self.refresh_data_bindings()







 


