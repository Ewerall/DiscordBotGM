from pprint import pprint

from datetime import datetime
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'credentials.json'
spreadsheet_id = '1ecawqy0N8Bpo0Fh_nyONZZxv9MRFTHdKaZVTeFCGdQI'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

def findColumn():
    b = 2
    f = 3
    while True:
        try:
            value = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range='B%d' % b,
                majorDimension = 'COLUMNS',
                valueRenderOption = 'UNFORMATTED_VALUE'
            ).execute()
            s = value['values']
            b += 1
            f += 1
        except KeyError:
            break
    return b, f

def addToTable(date):
    list = findColumn()
    time = datetime.today()
    strtime = time.strftime("%d/%m/%Y")
    service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": "B%d:F%d" % list,
                 "majorDimension": "ROWS",
                 "values": date},
            ]
        }
    ).execute()
    service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": "A%d" % list[0],
                 "majorDimension": "ROWS",
                 "values": [[strtime]]},
            ]
        }
    ).execute()