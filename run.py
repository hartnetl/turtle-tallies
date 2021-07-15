import gspread
from google.oauth2.service_account import Credentials

# These are the APIs needed to access the google sheet data
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('turtle_tallies')

raw_data = SHEET.worksheet('raw_data')
new_green = SHEET.worksheet('green_21')
green_20 = SHEET.worksheet('green_20')
new_logger = SHEET.worksheet('log_21')
logger_20 = SHEET.worksheet('log_20')
data_stock = SHEET.worksheet('admin')

rawdata = raw_data.get_all_values()
newg = new_green.get_all_values()
lastg = green_20.get_all_values()
newl = new_logger.get_all_values()
lastl = logger_20.get_all_values()
datal = data_stock.get_all_values()

print(datal)
