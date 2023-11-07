import gspread
from google.oauth2.service_account import Credentials

# Configurar as credenciais do OAuth2
credentials = Credentials.from_service_account_file('client_secret_775679487471-fsj4kf2b8rqn1f9nl7nhra47lc14mu47.apps.googleusercontent.com.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])

# Autenticar usando as credenciais
gc = gspread.authorize(credentials)

# Abra a planilha pelo seu ID ou URL
spreadsheet = gc.open_by_key('https://docs.google.com/spreadsheets/d/1cwDPhDXBbnIYqMjzxfGkPMOPQnzX2H0Tr1YtuVKJiQc/edit#gid=0')

# Selecione a planilha desejada
worksheet = spreadsheet.get_worksheet(0)  # 0 representa a primeira planilha na lista

# Alimente os dados na planilha
data_to_insert = ["Dado 1", "Dado 2", "Dado 3"]
worksheet.append_row(data_to_insert)
