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
    """
    Provide help info for users if needed
    """
    print("HELP")
    print('Headings:')
    print("DATE, SPECIES, ID, LOCATION, NEST(Y/N), DATA LOGGER (Y/N)")
    print("For 'DATE' enter the date the turtle or nest was observed in format day/month/year")
    print("For 'SPECIES', enter 'GREEN' for Green Sea Turtle or 'LOG' for Loggerhead Turtle")
    print("For 'ID' enter the id code on the turtle's flipper tag, which is CY followed by 4 digits")
    print("For 'LOCATION' enter B1 or B2 for the beach that you observed the turtle or nest")
    print("For 'NEST' type 'Y' if a nest was successfully laid, or 'N' if the nest and egg laying was not completed")
    print("For 'DATA LOGGER' type 'Y' if a data logger was placed in the nest, and 'N' if it wasn't. Type NA if no nest was laid.")
    print()
    print('Examples:')
    print("01/06/2021, LOG, CY0000, B1, Y, Y")
    print("01/06/2021, GREEN, CY0101, B2, N, NA\n")


def collect_raw_data():
    """
    User inputs the collected raw data and it is added to the raw data worksheet.
    """
    print("Enter latest nesting data")
    print("Type 'help' if you need information on the correct format\n")
    print("Note, this ^ functionality will be added later")

    user_data = input("Enter the data here: ")

    print(f"The data you provided here is '{user_data}'")
    print()

    # Convert data to csv formatting to go into the spreadsheet
    data_to_csv = user_data.split(",")

    check = input("Is this correct? (Y/N) ")
    user_verifiy_input(check)

    user_data_validation(data_to_csv)


def user_verifiy_input(letter):
    if letter == "Y":
        pass
    else:
        print("Try again\n")
        collect_raw_data()


def user_data_validation(userDataList):
    """
    First checks if user called for help. Returns the help function if they did. 
    Checks data is in correct format, as per the help guide:
    There must be 6 values entered.
    Date in day/month/year,  species is "LOG" or "Green", ID is string of letters and numbers,
    Location is B1 or B2, Nest is Y or N, Data logger is Y or N
    """
    try:
        if userDataList[0] == "help" or userDataList[0] == "Help" or userDataList[0] == "HELP":
            help()
            collect_raw_data()
        elif len(userDataList) != 6:
            raise ValueError(f"You must fill in all 6 fields, you only entered {len(userDataList)}")
    except ValueError as e:
        print(f"Something went wrong: {e}, try again \n")


collect_raw_data()
