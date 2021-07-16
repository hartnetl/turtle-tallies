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
info = SHEET.worksheet('admin')

# data = raw_data.get_all_values()
# print(data)


def welcome():
    print("""
                                                    ,'
                                                  ,;
                                                .'/
           `-_                                .'.'
             `;-_                           .' /
               `.-.        ,_.-'`'--'`'-._.` .'
                 `.`-.    /    .'"'.   _.'  /
                   `. '-.'_.._/0 " 0\/`    {\.
                     `.      |'-^Y^- |     //
                      (`\     \_."._/\...-;..-.
                      `._'._,'` ```    _.:---''`
                         ;-....----'''`
                        /   (
                        |  (`
                        `.^'
    """)

    print("""
               ╔╦╗╦ ╦╦═╗╔╦╗╦  ╔═╗  ╔╦╗╔═╗╦  ╦  ╦╔═╗╔═╗
                ║ ║ ║╠╦╝ ║ ║  ║╣    ║ ╠═╣║  ║  ║║╣ ╚═╗
                ╩ ╚═╝╩╚═ ╩ ╩═╝╚═╝   ╩ ╩ ╩╩═╝╩═╝╩╚═╝╚═╝
    """)


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
    User inputs the collected raw data.
    """
    # Prompt the user to input the data, or ask for help on how to format it
    print("Enter latest nesting data")
    print("Type 'help' if you need information on the correct format\n")

    user_data = input("Enter the data here:\n ")

    # Return the input data by the user for them to double check it is correct
    print(f"The data you provided here is '{user_data}'\n")

    # Call a function to continue if they say yes(Y), or restart if they say no (N)
    check = input("Is this correct? (Y/N) \n")
    user_verifiy_input(check)

    # Convert data to csv formatting to go into the spreadsheet
    data_to_csv = user_data.split(",")
    user_data_validation(data_to_csv)


def user_verifiy_input(letter):
    """
    This checks if the user is sure they have entered the correct data.
    If yes, the program continues.
    If no, it asks for the data to be entered again.
    """
    if letter == "Y" or letter == "y":
        pass
    else:
        print("Try again\n")
        collect_raw_data()


def user_data_validation(userDataList):
    """
    First checks if user called for help. Returns the help function if they
    did.
    Checks data is in correct format, as per the help guide:
    There must be 6 values entered.
    Date in day/month/year,  species is "LOG" or "Green", ID is string of
    letters and numbers,
    Location is B1 or B2, Nest is Y or N, Data logger is Y or N
    """
    try:
        if userDataList[0] == "help" or userDataList[0] == "Help" or userDataList[0] == "HELP":
            help()
            collect_raw_data()
        elif len(userDataList) != 6:
            raise ValueError(
                f"You must fill in all 6 fields, you only entered {len(userDataList)}"
            )
        # Data validation needed here
        elif userDataList[1].upper() != "LOG" and userDataList[1].upper() != "GREEN":
            raise NameError(
                f"You must enter 'LOG' or 'GREEN', you entered {userDataList[1]}"
            )
        elif len(userDataList[2]) != 6:
            raise ValueError(
                f"The ID should be CY followed by 4 digits, you entered {userDataList[2]}. Try again"
            )
        elif userDataList[3].upper() != "B1" and userDataList[3].upper() != "B2":
            raise NameError(
                f"You must enter 'B1' or 'B2', you entered {userDataList[3]}"
            )
        elif userDataList[4].upper() != "Y" and userDataList[4].upper() != "N":
            raise NameError(
                f"You must enter 'Y' or 'N' for nest, you entered {userDataList[4]}"
            )
        elif userDataList[5].upper() != "Y" and userDataList[5].upper() != "N":
            raise NameError(
                f"You must enter 'Y' or 'N' for nest, you entered {userDataList[5]}"
            )
    except ValueError as e:
        print(f"Something went wrong: {e}, try again")
        collect_raw_data()
    except NameError as e:
        print(f"You entered the wrong values: {e}, try again")
        collect_raw_data()
    finally:
        print("Validation complete")
        send_data_to_worksheets(userDataList)


def send_data_to_worksheets(data):
    """
    After validation, the data input by the user is added to the raw data worksheet.
    """
    print("Updating the worksheet...\n")
    upper_data = [item.upper() for item in data]
    raw_data.append_row(upper_data)
    print("Raw datasheet update complete!\n")
   
    if upper_data[1] == "LOG":
        upper_data.remove('LOG')
        new_logger.append_row(upper_data)
        print("Data also sent to log_21 worksheet")
    elif upper_data[1] == "GREEN":
        upper_data.remove('GREEN')
        new_green.append_row(upper_data)
        print("Data also sent to green_21 worksheet")


def calculate_total_nests():
    """
    Counts the number of nests laid in raw data sheet
    """
    nest_col = raw_data.col_values(5)
    total = 0
    for item in nest_col:
        if item == "Y":
            total += 1
    print("Calculating total nests")
    return total


def append_total_nests(total):
    """
    Updates the total nest value in admin worksheet and returns total to user
    """
    info.update('B2', total)
    updated = info.acell('B2').value
    print("Updating total in admin worksheet")
    print(f"{updated} nests have been laid this season so far!")


def calculate_green_and_logger_nests():
    """
    Calculates and returns how many nests have been laid by logger 
    and green turtles this season so far
    """
    


def calculate_data_logger_stock():
    """
    Updates number of data loggers left
    """
    data_logs = raw_data.col_values(6)
    logs = info.acell('A2').value
    total = int(logs)
    for item in data_logs:
        if item == "Y":
            total -= 1
    print("Calculating data loggers left")

    info.update("A2", total)
    print("Updating data log stock value")
    updated = info.acell('A2').value
    print(f"You have {updated} data loggers left")


# def calculate_difference():
#     """
#     Calculate and return the number of green and
#     logger turtle nests laid compared to last year
#     """
#     print("Calculating difference in nest numbers compared to last year")
#     last_green = int(green_20.acell('F2').value
#     this_green = int(info.acell(''))


# welcome()
collect_raw_data()
total = calculate_total_nests()
append_total_nests(total)
calculate_data_logger_stock()
# calculate_difference()

# 01/06/2021,LOG,CY1234,b1,y,y
# raw_data = SHEET.worksheet('raw_data')
# new_green = SHEET.worksheet('green_21')
# green_20 = SHEET.worksheet('green_20')
# new_logger = SHEET.worksheet('log_21')
# logger_20 = SHEET.worksheet('log_20')
# info = SHEET.worksheet('admin')
