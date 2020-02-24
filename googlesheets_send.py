import os
import apiclient
import urllib3
import json, re
from google.oauth2 import service_account
from googleapiclient import discovery
from datetime import datetime
import slack_post

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

Google_credz = os.environ.get('Google_credz')
print(type(Google_credz))

secret_file = json.loads(Google_credz)
print(type(secret_file))

secret_file2 = json.dumps(Google_credz)
print(type(secret_file2))

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1_2vJ8d2x5fpifx-D7sdmt6IReM9m_f-J1bpCiAt_TaE'


def send(data):
    #print(data)
    RANGE_NAME = 'Data!A:E'

    credentials = service_account.Credentials.from_service_account_info(secret_file, scopes=SCOPES)
    service = discovery.build('sheets','v4', credentials=credentials)
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=RANGE_NAME).execute()

    #values = result.get('values', [])
    message_text = json.dumps(data["event"]["text"])

    googledoc_URL = re.search('[^\s]+(?:docs.google.com)[^\s]+', message_text)
    time_sent = data["event"]["ts"]
    message_ID = data["event_id"]

    list = [[str(googledoc_URL.group(0)),time_sent,message_ID]]
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


def reaction(data):
    RANGE_NAME = 'Data!A:E'
    credentials = service_account.Credentials.from_service_account_info(secret_file, scopes=SCOPES)
    service = discovery.build('sheets','v4', credentials=credentials)
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=RANGE_NAME).execute()
    print(result)

    for index, sublist in enumerate(result["values"]):
        if data["event"]["item"]["ts"] in sublist:
            row_to_delete = 'A'+str((index+1))+':E'+ str((index+1))
            request_body = {}
            request = service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range=row_to_delete, body=request_body)
            response = request.execute()
            break

        else:
            print(data["event"]["item"]["ts"])

def check_spreadsheet():

    print("checking spreadsheet")
    RANGE_NAME = 'Data!A:E'
    credentials = service_account.Credentials.from_service_account_info(secret_file, scopes=SCOPES)
    service = discovery.build('sheets','v4', credentials=credentials)
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=RANGE_NAME).execute()


    for index, sublist in enumerate(result["values"]):
        if len(sublist) > 1:
            time_posted = datetime.fromtimestamp(sublist[1])
            print("found a timestamp" + str(time_posted)
            if time_posted.date < datetime.datetime.now()-datetime.timedelta(days=2):
                slack_message = []
                slack_message["text"] = "This hasn't been picked up in 2 days. SOMEONE DO IT NOOOOOOOOOWWWWWWWWWW" + sublist[0]
                print(slack_message["text"])
                slack_message["attachments"] = []
                slack_post.post(slack_message)
                break



if __name__ == '__main__':
    send()
