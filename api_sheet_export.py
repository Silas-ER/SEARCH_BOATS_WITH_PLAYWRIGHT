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

#values.get() ler -> values.update() escrever
def write_sheet(list_of_data):
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
        values_to_export = list_of_data  # assuming list_of_data is already in the correct format

        # Add more validation or manipulation of data if needed

        # Now, values_to_export is in the format expected by the API
        body = {"values": values_to_export}

        result = (
            sheet.values()
            .update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=SAMPLE_RANGE_NAME,
                body=body,
                valueInputOption="RAW",
            )
            .execute()
        )

        print("Updated values:", result)

    except HttpError as err:
        print("Error updating sheet:", err)
