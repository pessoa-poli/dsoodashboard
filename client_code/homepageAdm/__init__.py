from ._anvil_designer import homepageAdmTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
from ..legenda import legenda


class homepageAdm(homepageAdmTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.usuario_logado = anvil.server.call('return_current_user')
    self.init_components(**properties)   
    # Any code you write here will run when the form opens. 
    self.label_atualizacaodata.text = f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"    
    self.repeating_panel_warnings.items = anvil.server.call('busca_crises', idUsuario=self.usuario_logado['id'])    
    self.dropdown_andar.items = ["1º Andar", "2º Andar", "3º Andar"]
    self.dropdown_andar.selected_value = self.dropdown_andar.items[0]
    self.dropdown_bloco.items = ["Bloco A","Bloco B","Bloco C","Bloco D","Bloco E","Bloco F","Bloco G","Bloco H",]
    self.dropdown_bloco.selected_value = self.dropdown_bloco.items[7]
    self.hide_markers()
    self.setup_FloorPlan_Markers("H-111")
    self.visao_geral_link.underline = True
    self.setupData()
    if self.repeating_panel_warnings.items == None:
      self.repeating_panel_warnings.items = [{'nomeInstalacao':"none",
                                              "tipoNotificacao":"none",
                                              "nomeUsuario":"none"}]
    
  def h111_marker_mouse_down(self, x, y, button, **event_args):
    responsavel = anvil.server.call('buscar_responsavel', meuid='h111')    
    myvar = alert(content=ambiente_popup(responsavel=responsavel),
               large=True,
               buttons=[],
               dismissible=True)
    
  def setupData(self, **event_args):    
    lista_salas = anvil.server.call('get_lista_salas')
    self.salas_repeating_panel.items = lista_salas
    self.label_total_salas.text = len(lista_salas)   
    self.label_alto_risco.text = str(len([cat for cat in lista_salas if cat['nivelRisco']==3]))
    self.label_medio_risco.text = str(len([cat for cat in lista_salas if cat['nivelRisco']==2]))
    self.label_baixo_risco.text = str(len([cat for cat in lista_salas if cat['nivelRisco']==1]))
    qtd_pessoas = 0
    for cat in lista_salas:
        qtd_pessoas += cat['qtdPessoas']
    self.label_qtd_usuarios.text = qtd_pessoas
    
  def hide_markers(self, **event_args):
    self.h111_co2_image.visible = False    
    self.h111_overcapacity_image.visible = False         
    self.h111_maintenance_image.visible = False   
    self.h111_broom_image.visible = False    
    self.h111_green_marker.visible = False    
    self.h111_red_marker.visible = False   
    self.h111_yellow_marker.visible = False   
    self.h111_ok_image.visible = False
  
  #This function will server to parse the name of the images overlapping the floor plan,
  #    finding out to what room it belongs and then querying the database to find out whether 
  #    given marker should be visible.
  def findMarkerInfo(self, a_string, **event_args):
    markerInfo = {'room':"", 'type':''}
    firstUnderscore = a_string.find("_")
    markerInfo['room'] = f'{a_string[:1].upper()}-{a_string[1:firstUnderscore]}'
    secondPartOfString = a_string[firstUnderscore+1:]
    secondUnderscore = secondPartOfString.find("_")
    markerInfo['type'] = secondPartOfString[:secondUnderscore]
    return markerInfo
  
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


  def reload_dados(self, **event_args):
    self.setupData()    
    self.setup_FloorPlan_Markers(room="H-111")
    
  def link_sair_click(self, **event_args):
    anvil.server.call('logout')
    open_form('homepageComum')
    n = Notification("Logout efetuado com sucesso")
    n.show()

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

  def limpeza_link_click(self, **event_args):
    open_form('homepageLimpeza')  
  
  def timer_1_tick(self, **event_args):
    with anvil.server.no_loading_indicator:
      self.label_atualizacaodata.text = f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
      self.reload_dados()
      lista_crises = anvil.server.call('busca_novas_crises',
                                       idUsuario=self.usuario_logado['id'],
                                       listaCrisesVelha=self.repeating_panel_warnings.items)
      if len(lista_crises ) > 0:
        self.repeating_panel_warnings.items=lista_crises
      self.setup_FloorPlan_Markers()

  def link_legenda_click(self, **event_args):
    alert(content=legenda(), buttons=[], large=True)

  def button_legenda_click(self, **event_args):
    alert(content=legenda(), buttons=[], large=True)



 


