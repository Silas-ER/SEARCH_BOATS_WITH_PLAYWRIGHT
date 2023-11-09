import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1HlZCxbtphqKe8E3sQz6hVlptkKGiv3j3vDS7DM9OikA"
SAMPLE_RANGE_NAME = "dados!A2:D25"

list_of_data = [
  ["01/11/2023",	"CAMBORI"	,"6°34.741′ S",	"26°52.677′ W"],
  ["01/11/2023",	"DONA ILVA"	,"6°34.741′ S",	"26°52.677′ W"], 
  ["01/11/2023",	"IBIZA"	,"5°33.610′ S",	"23°58.578′ W"], 
  ["01/11/2023",	"MARIA CLARA"	,"5°46.921′ S",	"23°25.901′ W"], 
  ["01/11/2023",	"KOPESCA"	,"6°33.398′ S",	"29°31.830′ W"], 
  ["01/11/2023",	"KOWALSKI V",	"34°42.377′ S",	"46°13.481′ W"], 
  ["01/11/2023",	"MARBELLA I", "26°52.460′ S",	"48°43.532′ W"], 
  ["01/11/2023",	"KR III	2","6°52.966′ S",	"48°40.549′ W"], 
  ["01/11/2023",	"NATAL PESCA VII"	,"5°42.009′ S","	35°1.150′ W"], 
  ["01/11/2023",	"OULED SI MOHAND"	,"6°14.783′ S",	"26°12.551′ W"], 
  ["01/11/2023",	"NATAL PESCA IX",	"7°4.972′ S", "26°6.993′ W"], 
  ["01/11/2023",	"RIO JAPURA"	,"5°46.691′ S",	"35°12.451′ W"], 
  ["01/11/2023",	"RIO POTENGI"	,"5°57.852′ S",	"29°49.855′ W"], 
  ["01/11/2023",	"TUNASA I",	"6°1.713′ S", "23°8.523′ W"], 
  ["01/11/2023",	"LEAL SANTOS 7"	,"3°42.170′ S",	"38°35.580′ W"], 
  ["01/11/2023",	"MARLIN II"	,"6°46.919′ S", "24°1.720′ W"], 
  ["01/11/2023",	"MUCURIPE III"	,"6°32.900′ S",	"23°54.431′ W"], 
  ["01/11/2023",	"NETUNO S"	,"6°32.900′ S",	"23°54.431′ W"], 
  ["01/11/2023",	"TRANSMAR I", "0°55.193′ N",	"29°20.993′ W"], 
  ["01/11/2023",	"AZTECA III",	"6°9.314′ S",	"29°36.307′ W"], 
  ["01/11/2023",	"GUADALAJARA"	,"7°11.473′ S",	"24°25.769′ W"],
  ["01/11/2023",	"STA PAULINA"	,"5°46.587′ S",	"33°33.856′ W"], 
  ["01/11/2023",	"ROMULO"	,"5°57.498′ S",	"28°52.822′ W"],
  ["01/11/2023",	"FILHO DA PROMESSA"	,"5°43.191′ S",	"23°42.651′ W"]
]

#values.get() ler -> values.update() escrever
def main():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        # Prepare the values to be updated
        body = {"values": list_of_data}

        result = (
            sheet.values()
            .update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=SAMPLE_RANGE_NAME,
                body=body,
                valueInputOption="RAW",  # Specify how input values should be interpreted
            )
            .execute()
        )

    except HttpError as err:
        print(err)

if __name__ == "__main__":
  main()
""" 
    #ler dados
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
        .execute()
    )
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return
    
    for row in values:
      print(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}")
  
"""