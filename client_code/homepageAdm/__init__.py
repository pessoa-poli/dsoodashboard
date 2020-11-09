from ._anvil_designer import homepageAdmTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .ambiente_popup import ambiente_popup
from ..telaUsuarios import telaUsuarios

class homepageAdm(homepageAdmTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)    
    # Any code you write here will run when the form opens.
    self.repeating_panel_warnings.items = ["H-111"]
    self.setupData()
    self.dropdown_andar.items = ["1º Andar", "2º Andar", "3º Andar"]
    self.dropdown_andar.selected_value = self.dropdown_andar.items[0]
    self.dropdown_bloco.items = ["Bloco A","Bloco B","Bloco C","Bloco D","Bloco E","Bloco F","Bloco G","Bloco H",]
    self.dropdown_bloco.selected_value = self.dropdown_bloco.items[7]
    self.hide_markers()
    self.setup_FloorPlan_Markers("H-111")
    self.visao_geral_link.underline = True
    
  def h111_marker_mouse_down(self, x, y, button, **event_args):
    responsavel = anvil.server.call('buscar_responsavel', meuid='h111')    
    myvar = alert(content=ambiente_popup(responsavel=responsavel),
               large=True,
               buttons=[],
               dismissible=True)
    
  def setupData(self, **event_args):
    self.salas_repeating_panel.items = anvil.server.call('get_lista_salas')
    self.label_total_salas.text = str(self.getTotalUsuarios())
    self.label_alto_risco.text = str(anvil.server.call('get_count_salas_alto_risco'))
    self.label_medio_risco.text = str(anvil.server.call('get_count_salas_medio_risco'))
    self.label_baixo_risco.text = str(anvil.server.call('get_count_salas_baixo_risco'))
    self.label_qtd_usuarios.text = str(anvil.server.call('get_count_usuarios_presentes'))
    
  def hide_markers(self, **event_args):
    self.h111_co2_image.visible = False    
    self.h111_overcapacity_image.visible = False         
    self.h111_maintenance_image.visible = False   
    self.h111_broom_image.visible = False    
    self.h111_green_marker.visible = False    
    self.h111_red_marker.visible = False   
    self.h111_yellow_marker.visible = False   
    self.h111_ok_image.visible = False

  def setup_FloorPlan_Markers(self, room=None, **event_args):
    markers_list = self.xy_panel_1.get_components()
    sala = anvil.server.call('get_sala_pelo_nome', nome_sala=room)
    print(sala)
    critico = False
    
    for component in markers_list:
      if component.name == f'{room}_ok_image':
        pass
      if component.name == f'{room}_broom_image':
        pass
      if component.name == f'{room}_co2_image':
        pass
      if component.name == f'{room}_maintenance_image':
        pass
      if component.name == f'{room}_overcapacity_image':
        pass
      if component.name == f'{room}_green_marker':
        pass
      if component.name == f'{room}_yellow_marker':
        pass
      if component.name == f'{room}_red_marker':
        pass
    
    if sala['co2'] >= 700:
      self.h111_co2_image.visible = True
      critico = True
    else:
      self.h111_co2_image.visible = False
    if sala['capacidadeUltrapassada']:
      self.h111_overcapacity_image.visible = True
      critico = True
    else:
      self.h111_overcapacity_image.visible = False
    if sala['necessitaManutencao']:      
      self.h111_maintenance_image.visible = True
      critico = True
    else:
      self.h111_maintenance_image.visible = False
    if sala['necessitaLimpeza']:
      self.h111_broom_image.visible = True
      critico = True
    else:
      self.h111_broom_image.visible = False
    if sala['nivel_risco']['risco'] == "verde":
      self.h111_green_marker.visible = True
    if sala['nivel_risco']['risco'] == "vermelho":
      self.h111_red_marker.visible = True
    if sala['nivel_risco']['risco'] == "amarelo":
      self.h111_yellow_marker.visible = True
    if not critico:
      self.h111_ok_image.visible = True
    else:
      self.h111_ok_image.visible = False

  def reload_dados(self, **event_args):
    self.setupData()
    self.refresh_data_bindings()
    self.setup_FloorPlan_Markers(room="H-111")
    
  def link_sair_click(self, **event_args):
    anvil.users.logout()
    open_form('homepageComum')

  def h111_marker_mouse_down(self, x, y, button, **event_args):
    responsavel = anvil.server.call('buscar_responsavel', meuid='h111')    
    myvar = alert(content=ambiente_popup(responsavel=responsavel),
               large=True,
               buttons=[],
               dismissible=True)

  def usuarios_link_click(self, **event_args):
    open_form('telaUsuarios')

  def getTotalUsuarios(self):
    valor = 0    
    for inst in self.salas_repeating_panel.items:
      valor += inst['qtdPessoas']
    return valor
    
  def timer_1_tick(self, **event_args):
    with anvil.server.no_loading_indicator:
      self.reload_dados()


 


