import os
import apiclient
import urllib3
import json, re
from google.oauth2 import service_account
from googleapiclient import discovery

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

Google_credz = os.environ.get('Google_credz')
print(type(Google_credz))

secret_file = json.loads(Google_credz)
print(type(secret_file))

secret_file2 = json.dumps(Google_credz)
print(type(secret_file2))

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1_2vJ8d2x5fpifx-D7sdmt6IReM9m_f-J1bpCiAt_TaE'
RANGE_NAME = 'Data!A:E'

def send(data):
    #print(data)

    credentials = service_account.Credentials.from_service_account_info(secret_file, scopes=SCOPES)
    service = discovery.build('sheets','v4', credentials=credentials)
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=RANGE_NAME).execute()

    #values = result.get('values', [])
    message_text = json.dumps(data["event"]["text"])
    googledoc_URL = re.search('[^\s]+(?:docs.google.com)[^\s]+', message_text)
    list = [[googledoc_URL.group(0)]]
    resource = {
        "range": 'Data!A:E',
        "majorDimension": "ROWS",
        "values": list
    }

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        body=resource,
        valueInputOption="USER_ENTERED"
    ).execute()






if __name__ == '__main__':
    send()
