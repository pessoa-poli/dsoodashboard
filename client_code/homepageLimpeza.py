from ._anvil_designer import homepageLimpezaTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

class homepageLimpeza(homepageLimpezaTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    #logou = anvil.server.call('login', 'teste@teste.com', 'testesenha', lembrardemim=False)
    self.usuario_logado = anvil.server.call('return_current_user')
    self.dropdown_andar.items = ["1º Andar", "2º Andar", "3º Andar"]
    self.dropdown_andar.selected_value = self.dropdown_andar.items[0]
    self.dropdown_bloco.items = ["Bloco A","Bloco B","Bloco C","Bloco D","Bloco E","Bloco F","Bloco G","Bloco H",]
    self.dropdown_bloco.selected_value = self.dropdown_bloco.items[7]  
    self.repeating_panel_limpeza.set_event_handler('x-refresh-panels', self.refresh_panels)
    self.label_atualizacaodata.text = f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"    
    
    self.init_components(**properties)
    
    # Any code you write here will run when the form opens.
    
    self.hide_markers()
    self.setup_FloorPlan_Markers(1)
    self.repeating_panel_limpeza.items = anvil.server.call('buscar_instalacoes_responsabilizadas_limpeza', self.usuario_logado['id'])
    self.repeating_panel_warnings.items = anvil.server.call("busca_crises", idUsuario=self.usuario_logado['id'])
    
  def refresh_panels(self, **event_args):    
    self.repeating_panel_limpeza.items = anvil.server.call('buscar_instalacoes_responsabilizadas_limpeza', self.usuario_logado['id'])
    self.repeating_panel_warnings.items = anvil.server.call("busca_crises", idUsuario=self.usuario_logado['id'])
    
  def h111_marker_mouse_down(self, x, y, button, **event_args):
    responsavel = anvil.server.call('buscar_responsavel', meuid='h111')    
    myvar = alert(content=ambiente_popup(responsavel=responsavel),
               large=True,
               buttons=[],
               dismissible=True)

  def link_sair_click(self, **event_args):
    anvil.server.call('logout')
    open_form('homepageComum')
    n = Notification("Logout efetuado com sucesso")
    n.show()
    
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


  def visao_geral_link_click(self, **event_args):
    open_form('homepageAdm')

  def link_1_click(self, **event_args):
    open_form('telaUsuarios')

  def timer_1_tick(self, **event_args):
    with anvil.server.no_loading_indicator:
      self.label_atualizacaodata.text = f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
      self.repeating_panel_limpeza.items = anvil.server.call('buscar_instalacoes_responsabilizadas_limpeza', self.usuario_logado['id'])
      self.repeating_panel_warnings.items = anvil.server.call("busca_crises", self.usuario_logado['id'])
  


