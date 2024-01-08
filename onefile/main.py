from playwright.sync_api import sync_playwright
import time, re, datetime, folium, os.path, smtplib
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

#LER DADOS DOS ARQUIVOS
def read_credentials(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if len(lines) < 2:
            raise ValueError("O arquivo de credenciais não contém informações suficientes.")
        username = lines[0].strip().split(':')[-1].strip()
        password = lines[1].strip().split(':')[-1].strip()
        return username, password

def read_dados_boats(file_path):
    dados_boats = []  # Inicializa uma lista vazia para armazenar os dados dos barcos
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Verifique se a linha contém "NAME:" e "MMSI:" antes de processá-la
            if "NAME:" in line and "MMSI:" in line:
                name = line.split("NAME: ")[1].split(",")[0].strip()
                mmsi = line.split("MMSI: ")[1].strip()
                dados_boats.append({'name': name, 'mmsi': mmsi})  # Adiciona os dados à lista
    return dados_boats

def read_smtp(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        server = lines[0].strip().split(':')[-1].strip()
        port = lines[1].strip().split(':')[-1].strip()
        user = lines[2].strip().split(':')[-1].strip()
        password = lines[3].strip().split(':')[-1].strip()
        return server, port, user, password

def read_adressees(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        email_address = lines[0].strip().split(':')[-1].strip()
        return email_address

def to_convert(dms_str):
    # Usando expressões regulares para extrair os valores numéricos e a direção
    match = re.match(r'(\d+)°(\d+\.\d+)′\s*([NSEW])', dms_str)
    if match:
        degrees = float(match.group(1))
        minutes = float(match.group(2))
        direction = match.group(3)
        
        # Convertendo os graus e minutos para decimal
        decimal_degrees = degrees + (minutes / 60.0)
        
        # Verificando a direção (N, S, E, W) e aplicando o sinal correto para latitude ou longitude
        if direction == 'S' or direction == 'W':
            decimal_degrees = -decimal_degrees
        
        return decimal_degrees
    else:
        return None

#FUNÇÃO PARA GERAR MAPA
def create_map(list):
    mapa = folium.Map(location=[-5.812757, -35.255127], zoom_start=6)  

    for pin in list:
        popup_text = f"<h5>{pin['name']}</h5><p>Latitude: {pin['lat']}<br>Longitude: {pin['long']}</p>"
        folium.Marker([pin['lat'], pin['long']], popup=popup_text).add_to(mapa)

    return mapa

#FUNÇÃO PARA ATUALIZAR PLANILHA
def append_to_sheet(list_data):
    token_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token.json")
    client_secret_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "client_secret.json")
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"] # If modifying these scopes, delete the file token.json.
    SAMPLE_SPREADSHEET_ID = "1HlZCxbtphqKe8E3sQz6hVlptkKGiv3j3vDS7DM9OikA" # The ID and range of a sample spreadsheet.
    SAMPLE_RANGE_NAME = "dados"

    creds = None

    if os.path.exists(token_file_path):
        creds = Credentials.from_authorized_user_file(token_file_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_path, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(token_file_path, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        # Prepare the values to be appended
        values_to_append = list_data  # assuming list_of_data is already in the correct format

        body = {"values": values_to_append} # Now, values_to_append is in the format expected by the API

        result = (
            sheet.values()
            .append(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=SAMPLE_RANGE_NAME,
                body=body,
                valueInputOption="RAW",
            )
            .execute()
        )

        print("Appended values:", result)

    except HttpError as err:
        print("Error appending to sheet:", err)

#FUNÇÃO PARA ENVIAR EMAIL
def send_email(serv, prt, usr, passw, date, adressees):
    smtp_server = serv  
    smtp_port = prt
    smtp_username = usr
    smtp_password = passw

    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = adressees
    msg['Subject'] = 'Localização dos barcos'

    body = f"Bom dia, Seguem anexo o HTML com os dados de localização dos barcos do dia {date}, o dados podem ser visualizados na planilha online: https://docs.google.com/spreadsheets/d/1HlZCxbtphqKe8E3sQz6hVlptkKGiv3j3vDS7DM9OikA/edit#gid=0. "
    msg.attach(MIMEText(body, 'plain'))

    with open(f'mapa_{date}.html', 'rb') as attachment:
        part = MIMEApplication(attachment.read(), Name=f'mapa_{date}.html')

    part['Content-Disposition'] = f'attachment; filename="mapa_{date}.html"'
    msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  
        server.login(smtp_username, smtp_password)

        server.sendmail(smtp_username, adressees, msg.as_string()) 
        print('Email enviado com sucesso')
    except Exception as e:
        print(f'Erro ao enviar email: {str(e)}')
    finally:
        server.quit()

#MAIN DO PROGRAMA
def main():
    #LEITURA DOS DADOS COM CAMINHOS ABSOLUTOS
    current_directory = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(current_directory, 'credentials.txt')
    dados_boats_path = os.path.join(current_directory, 'data_query.txt')
    smtp_path = os.path.join(current_directory, 'data_smtp.txt')
    adressees_path = os.path.join(current_directory, 'addressees.txt')

    #LEITURA DOS DADOS
    username, password = read_credentials(credentials_path)
    dados_boats = read_dados_boats(dados_boats_path)
    server, port, user, passw = read_smtp(smtp_path)
    email_address = read_adressees(adressees_path)

    #DATA ATUAL
    data_atual = datetime.datetime.now()
    data_formatada = data_atual.strftime("%d/%m/%Y") 
    data_formatada_to_save = data_atual.strftime("%d_%m_%Y")   

    #LISTA DE PARA ACRESCENTAR OS DADOS
    dados_exportar = []
    dados_convertidos = [] #dados convertidos para decimal

    #AUTOMAÇÃO
    try:
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

    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")

    #CONVERTER DADOS PARA DECIMAL
    for dados in dados_exportar:
        latitude_decimal = round(to_convert(dados[2]), 2)
        longitude_decimal = round(to_convert(dados[3]), 2)

        # Criar um dicionário com as chaves 'name', 'lat' e 'long'
        dados_convertidos.append({'name': dados[1], 'lat': latitude_decimal, 'long': longitude_decimal})

    #GERAR MAPA
    mapa = create_map(dados_convertidos)
    mapa.save(f'mapa_{data_formatada_to_save}.html')

    #EXPORTAR DADOS PARA PLANILHA
    append_to_sheet(dados_exportar)

    #ENVIAR EMAIL's
    send_email(server, port, user, passw, data_formatada_to_save, email_address)

#ABERTURA DA MAIN
if __name__ == '__main__':
    main()
