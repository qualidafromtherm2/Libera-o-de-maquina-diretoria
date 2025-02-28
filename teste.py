import gspread
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDS = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(CREDS)

SPREADSHEET_ID = "1wQtlPKVhkXNzsVTYfbEaXDkW9mSBHtkO2H5RV6KFxsY"
sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Rastreabilidade")
dados = sheet.get_all_values()
print(dados)
