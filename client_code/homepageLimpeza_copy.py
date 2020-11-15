from ._anvil_designer import homepageLimpeza_copyTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .homepageAdm import homepageAdm
from .telaUsuarios import telaUsuarios

class homepageLimpeza_copy(homepageLimpeza_copyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.dropdown_andar.items = ["1º Andar", "2º Andar", "3º Andar"]
    self.dropdown_andar.selected_value = self.dropdown_andar.items[0]
    self.dropdown_bloco.items = ["Bloco A","Bloco B","Bloco C","Bloco D","Bloco E","Bloco F","Bloco G","Bloco H",]
    self.dropdown_bloco.selected_value = self.dropdown_bloco.items[7]
    
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    self.hide_markers()
    self.setup_FloorPlan_Markers("h111")
    self.repeating_panel_limpeza.items = anvil.server.call('get_lista_salas')
    

  def h111_marker_mouse_down(self, x, y, button, **event_args):
    responsavel = anvil.server.call('buscar_responsavel', meuid='h111')    
    myvar = alert(content=ambiente_popup(responsavel=responsavel),
               large=True,
               buttons=[],
               dismissible=True)

  def link_sair_click(self, **event_args):
    anvil.users.logout()
    open_form('homepageComum')
    
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

  def visao_geral_link_click(self, **event_args):
    open_form('homepageAdm')

  def link_1_click(self, **event_args):
    open_form('telaUsuarios')


