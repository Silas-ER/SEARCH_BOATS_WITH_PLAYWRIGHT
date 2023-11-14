from playwright.sync_api import sync_playwright
import datetime
import time
from functions.api_sheet_export import write_sheet
from functions.read_data import read_credentials_from_file, read_dados_boats, to_convert


#COLETA DE DATA ATUAL 
data_atual = datetime.datetime.now()
data_formatada = data_atual.strftime("%d/%m/%Y")

def data_capture():
    #LISTA DE DADOS DA EXPORTAÇÃO 
    dados_exportar = []
    data_convert = []

    #LEITURA DE CREDENCIAIS E DADOS DO BARCO
    try:
        username, password = read_credentials_from_file('research_base/credenciais.txt')
        
    except Exception as e:
        print(f"Erro ao ler as credenciais: {str(e)}")
        exit(1)

    try:
        dados_boats = read_dados_boats('research_base/dados_consulta.txt')

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
        page.wait_for_selector('iframe[id="loginIframe"]', timeout=20000)
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


        for index, dados in enumerate(dados_boats):
            try:
                # Interact with the frame
                search_camp = frame_map.wait_for_selector('.ship_search_input', timeout=20000)
                if search_camp:
                    search_camp.fill(dados['mmsi'])

                search_result = frame_map.wait_for_selector('span.ship_name', timeout=20000)
                if search_result:
                    search_result.click()

                    # Aguarde a visibilidade dos elementos no pop-up
                    frame_map.wait_for_selector('div.poupWindowDetail span[name="shipposition"]', timeout=20000)
                    
                    data_latitude = frame_map.locator('div.poupWindowDetail span[name="shipposition"]').inner_text()
                    data_longitude = frame_map.locator('div.poupWindowDetail span[name="shiplonti"]').inner_text()

                    dados_exportar.append([data_formatada, dados['name'], data_latitude, data_longitude])

                    print(f'{dados["name"]} - Índice {index} ok!')

            except Exception as e:
                print(f"Erro durante a execução: {str(e)}")

        browser.close()

    for data in dados_exportar:

        date = data[0]
        name = data[1]
        lat = to_convert(data[2])
        long = to_convert(data[3])
        data_convert.append({'name': name, 'lat': lat, 'long': long})

    write_sheet(dados_exportar)

    return data_convert
