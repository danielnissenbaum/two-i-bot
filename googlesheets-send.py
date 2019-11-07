import os
from apiclient import discovery
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
secret_file = os.path.join("creds/","two-i.json")

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1_2vJ8d2x5fpifx-D7sdmt6IReM9m_f-J1bpCiAt_TaE'
SAMPLE_RANGE_NAME = 'Data!A1:E'

def send(data):
    print(data)

    credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=SCOPES)
    service = discovery.build('sheets','v4', credentials=credentials)
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=SAMPLE_RANGE_NAME).execute()

    values = result.get('values', [])

    



if __name__ == '__main__':
    send("you did what?")