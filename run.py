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

# Naming each worksheet in the document
raw_data = SHEET.worksheet('raw_data')
new_green = SHEET.worksheet('green_21')
green_20 = SHEET.worksheet('green_20')
new_logger = SHEET.worksheet('log_21')
logger_20 = SHEET.worksheet('log_20')
data_stock = SHEET.worksheet('admin')

# Help message for formatting the correct input
def help():
    print('Headings:')
    print("SPECIES, ID, LOCATION, NEST(Y/N), DATA LOGGER (Y/N)")
    print("For 'SPECIES', enter 'GREEN' for Green Sea Turtle or 'LOG' for Loggerhead Turtle")
    print("For 'ID' enter the id code on the turtle's flipper tag, which is CY followed by 4 digits")
    print("For 'LOCATION' enter B1 or B2 for the beach that you observed the turtle or nest")
    print("For 'NEST' type 'Y' if a nest was successfully laid, or 'N' if the nest and egg laying was not completed")
    print("For 'DATA LOGGER' type 'Y' if a data logger was placed in the nest, and 'N' if it wasn't. Type NA if no nest was laid.")
    print()
    print('Examples:')
    print("LOG, CY0000, B1, Y, Y")
    print("GREEN, CY0101, B2, N, NA")


def collect_raw_data():
    """
    User inputs the collected raw data and it is added to the raw data worksheet.
    """
    print("Enter latest nesting data")
    print("Type 'help' if you need information on the correct format\n")
    
    user_data = input("Enter the data here: ")
    print()
    print(f"The data you provided here is {user_data}")
    print()

    input("Is this correct? (Y/N) ")
    print("this worked")

collect_raw_data()
