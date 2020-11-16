from ._anvil_designer import dev_formTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class dev_form(dev_formTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.repeating_panel_1.items = anvil.server.call('busca_crises')
    self.init_components(**properties)
    self.results_dic = {}
    # Any code you write here will run when the form opens.

  def call_back_click(self, **event_args):
    count = anvil.server.call('get_total_salas')
    self.label_gettotalsalas.text = f"Total de salas {count['count']}"

  def button_getlistasalas_click(self, **event_args):
    lista_salas = anvil.server.call('get_lista_salas')
    

  def buscar_responsavel_click(self, **event_args):
    anvil.server.call('buscar_responsavel', nome_sala='H-111', limpeza=False)

  def get_sala_pelo_id_click(self, **event_args):
    sala = anvil.server.call('get_sala_pelo_nome', nome_sala="H-111")
    print(sala)

  def button_login_click(self, **event_args):
    didLogin = anvil.server.call('login', 'teste@teste.com', 'testesenha')
    print(didLogin)





