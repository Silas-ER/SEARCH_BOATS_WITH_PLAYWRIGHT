import os.path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

scopes = ['https://www.googleapis.com/auth/mymaps']

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", scopes)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json", scopes
        )
        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

# Substitua 'IDDoSeuMapa' pelo ID do seu mapa
MAPS_ID = '1xdFzD7dtzlHCk2QjJlswYtT9Yu6cf5o'

# Dados de exemplo - Substitua pelos seus próprios dados
data_to_update = [
    {"id": "01/11/2023", "nome": "CAMBORI", "latitude": "6°34.741′ S", "longitude": "26°52.677′ W"},
    {"id": "01/11/2023", "nome": "DONA ILVA", "latitude": "6°34.741′ S", "longitude": "26°52.677′ W"},
    # Adicione mais itens conforme necessário
]

def update_my_maps():
    # Inicializar o serviço da API do Google My Maps
    mymaps_service = build('mymaps', 'v3', credentials=creds)  # Use 'creds' em vez de 'credentials'

    for item in data_to_update:
        feature_id = item["id"]
        nome = item["nome"]
        latitude = item["latitude"]
        longitude = item["longitude"]

        # Construir o payload de atualização
        update_payload = {
            'name': nome,
            'latitude': latitude,
            'longitude': longitude,
            # Adicione mais campos conforme necessário
        }

        # Enviar a solicitação de atualização para a API do Google My Maps
        mymaps_service.maps().features().patch(mapId=MAPS_ID, featureId=feature_id, body=update_payload).execute()

if __name__ == "__main__":
    update_my_maps()


"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Substitua 'URLDoSeuMapa' pela URL do seu mapa no Google My Maps
MAP_URL = 'URLDoSeuMapa'

# Substitua 'CaminhoParaSeuDriverDoChrome' pelo caminho para o executável do ChromeDriver
CHROME_DRIVER_PATH = 'CaminhoParaSeuDriverDoChrome'

# Inicializar o driver do Chrome
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

# Abrir a URL do mapa
driver.get(MAP_URL)

# Esperar alguns segundos para o mapa carregar completamente
time.sleep(5)

# Substitua 'NomeDoMarcador' pelo nome do marcador que você deseja atualizar
marker_name = 'NomeDoMarcador'

# Encontrar o campo de pesquisa no mapa e inserir o nome do marcador
search_input = driver.find_element('id', 'searchboxinput')
search_input.clear()
search_input.send_keys(marker_name)
search_input.send_keys(Keys.ENTER)

# Esperar alguns segundos para a atualização ser refletida
time.sleep(5)

# Substitua 'NovoNome' pela nova informação que você deseja colocar no marcador
new_info = 'NovoNome'

# Encontrar o elemento de edição e inserir a nova informação
edit_button = driver.find_element('css selector', '.action-icon-mymaps-edit')
edit_button.click()

info_input = driver.find_element('css selector', '.widget-title-textbox')
info_input.clear()
info_input.send_keys(new_info)

# Salvar as alterações
save_button = driver.find_element('css selector', '.action-icon-mymaps-save')
save_button.click()

# Fechar o navegador
driver.quit()
"""