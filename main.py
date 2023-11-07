from playwright.sync_api import sync_playwright
import datetime
import time
from escrita_dados import exportar
from read_data import read_credentials_from_file, read_dados_boats

#COLETA DE DATA ATUAL 
data_atual = datetime.datetime.now()
data_formatada = data_atual.strftime("%d/%m/%Y")

#LISTA DE DADOS DA EXPORTAÇÃO 
dados_exportar = []

#LEITURA DE CREDENCIAIS E DADOS DO BARCO
try:
    username, password = read_credentials_from_file('credenciais.txt')
    
except Exception as e:
    print(f"Erro ao ler as credenciais: {str(e)}")
    exit(1)

try:
    dados_boats = read_dados_boats('dados_consulta.txt')

except Exception as e:
    print(f"Erro ao ler os dados dos barcos: {str(e)}")
    exit(1)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.shipdt.com/", timeout=200000)

    #clique no botao de login
    button_login_register = page.locator('.navbar-right .login')
    button_login_register.click()

    time.sleep(15)

    #frame do login 
    page.wait_for_selector('iframe[id="loginIframe"]')
    frame_login = page.frame('loginIframe')
    
    campo_email = frame_login.locator('input.ivu-input.ivu-input-large[placeholder="Phone Number/Email"]')
    campo_email.fill(username)

    campo_password = frame_login.locator('input.ivu-input.ivu-input-large[placeholder="Password"]')
    campo_password.fill(password)

    button_login = frame_login.locator('.loginButton.regBtn.ivu-btn.ivu-btn-primary.ivu-btn-long.ivu-btn-large')
    button_login.click()

    print("logado!")

    time.sleep(15)  

    # Saia do iframe
    page.bring_to_front()

    #frame do mapa
    frame_map = page.frame('iframeMap')

    time.sleep(35)

    for dados in dados_boats: 
        #Interact with the frame
        search_camp = frame_map.locator('.ship_search_input') 
        search_camp.fill(dados['mmsi'])

        time.sleep(50)

        search_result = frame_map.locator('span.ship_name')
        search_result.click()

        data_latitude = frame_map.locator('div.poupWindowDetail span[name="shipposition"]').inner_text()
        data_longitude = frame_map.locator('div.poupWindowDetail span[name="shiplonti"]').inner_text()

        dados_exportar.append({'data': data_formatada, 'name': dados['name'], 'latitude': data_latitude, 'longitude': data_longitude})

        print('{} ok!'.format(dados['name']))

        time.sleep(50)

    browser.close()

exportar(dados_exportar)