import gspread
from google.oauth2.service_account import Credentials
import sys
import time

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
    fast_print("""
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

    fast_print("""
               ╔╦╗╦ ╦╦═╗╔╦╗╦  ╔═╗  ╔╦╗╔═╗╦  ╦  ╦╔═╗╔═╗
                ║ ║ ║╠╦╝ ║ ║  ║╣    ║ ╠═╣║  ║  ║║╣ ╚═╗
                ╩ ╚═╝╩╚═ ╩ ╩═╝╚═╝   ╩ ╩ ╩╩═╝╩═╝╩╚═╝╚═╝..
    """)


# Credit for help with this function
# https://stackoverflow.com/questions/4099422/printing-slowly-simulate-typing
def type_print(str):
    """
    Prints text out letter by letter instead of all at once
    """
    for letter in str + '\n':
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(.8)


def fast_print(str):
    """
    Prints text out quickly letter by letter instead of all at once
    """
    for letter in str + '\n':
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(.01)


# Help message for formatting the correct input
def help():
    """
    Provide help info for users if needed
    """
    type_print("HELP")
    type_print('Headings:')
    type_print("DATE, SPECIES, ID, LOCATION, NEST(Y/N), DATA LOGGER (Y/N)")
    type_print("For 'DATE' enter the date the turtle or nest was observed in format day/month/year")
    type_print("For 'SPECIES', enter 'GREEN' for Green Sea Turtle or 'LOG' for Loggerhead Turtle")
    type_print("For 'ID' enter the id code on the turtle's flipper tag, which is CY followed by 4 digits")
    type_print("For 'LOCATION' enter B1 or B2 for the beach that you observed the turtle or nest")
    type_print("For 'NEST' type 'Y' if a nest was successfully laid, or 'N' if the nest and egg laying was not completed")
    type_print("For 'DATA LOGGER' type 'Y' if a data logger was placed in the nest, and 'N' if it wasn't. Type NA if no nest was laid.")
    type_print()
    type_print('Examples:')
    type_print("01/06/2021, LOG, CY0000, B1, Y, Y")
    type_print("01/06/2021, GREEN, CY0101, B2, N, NA\n")


def collect_raw_data():
    """
    User inputs the collected raw data.
    """
    # Prompt the user to input the data, or ask for help on how to format it
    type_print("Enter latest nesting data")
    type_print("Type 'help' if you need information on the correct format\n")

    user_data = input("Enter the data here:\n ")

    # Return the input data by the user for them to double check it is correct
    type_print(f"The data you provided here is '{user_data}'\n")

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
        type_print("Try again\n")
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
        type_print(f"Something went wrong: {e}, try again")
        collect_raw_data()
    except NameError as e:
        type_print(f"You entered the wrong values: {e}, try again")
        collect_raw_data()
    finally:
        type_print("Validation complete")
        send_data_to_worksheets(userDataList)


def send_data_to_worksheets(data):
    """
    After validation, the data input by the user is added to the raw data worksheet.
    """
    type_print("Updating the worksheet...\n")
    upper_data = [item.upper() for item in data]
    raw_data.append_row(upper_data)
    type_print("Raw datasheet update complete!\n")

    if upper_data[1] == "LOG":
        upper_data.remove('LOG')
        new_logger.append_row(upper_data)
        type_print("Data also sent to log_21 worksheet")
    elif upper_data[1] == "GREEN":
        upper_data.remove('GREEN')
        new_green.append_row(upper_data)
        type_print("Data also sent to green_21 worksheet")


def calculate_total_nests():
    """
    Counts the number of nests laid in raw data sheet
    """
    nest_col = raw_data.col_values(5)
    total = 0
    for item in nest_col:
        if item == "Y":
            total += 1
    type_print("Calculating total nests")
    return total


def append_total_nests(total):
    """
    Updates the total nest value in admin worksheet and returns total to user
    """
    info.update('B2', total)
    updated = info.acell('B2').value
    type_print("Updating total in admin worksheet")
    type_print(f"{updated} nests have been laid this season so far!")


def calculate_green_and_logger_nests():
    """
    Calculates and returns how many nests have been laid by loggerhead
    and green turtles this season so far
    """
    # Calculate greens first
    green_nest = new_green.col_values(4)
    green_total = 0
    type_print("Calculating green nests")
    for item in green_nest:
        if item == "Y":
            green_total += 1

    type_print("Adding to admin sheet")
    info.update('D2', green_total)
    green = info.acell('D2').value
    type_print(f"There have been {green} Green Sea Turtle nests laid so far this season")

    # Now the loggerheads
    logger_nest = new_logger.col_values(4)
    logger_total = 0
    type_print("Calculating logger nests")
    for items in logger_nest:
        if items == "Y":
            logger_total += 1

    type_print("Adding to admin sheet")
    info.update('E2', logger_total)
    logger = info.acell('E2').value
    type_print(f"There have been {logger} Loggerhead Turtle nests laid so far this season")


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
    type_print("Calculating data loggers left")

    info.update("A2", total)
    type_print("Updating data log stock value")
    updated = info.acell('A2').value
    type_print(f"You have {updated} data loggers left")


def calculate_difference():
    """
    Calculate and return the number of green and
    logger turtle nests laid compared to last year
    """
    type_print("Calculating difference in total nest numbers compared to last year")
    last_total = int(info.acell('C2').value)
    this_total = int(info.acell('B2').value)
    total_diff = last_total - this_total
    if total_diff > 0:
        type_print(f"There were {total_diff} more nests laid in total last year")
    elif total_diff < 0:
        type_print(f"There were {total_diff} less nests laid in total last year")
    elif total_diff == 0:
        type_print("The same amount of nests were laid last year")

    type_print("Calculating difference in green turtle nest numbers compared to last year")
    last_green = int(green_20.acell('F2').value)
    this_green = int(info.acell('D2').value)
    green_diff = last_green - this_green
    if green_diff > 0:
        type_print(f"There were {green_diff} more green nests laid last year")
    elif green_diff < 0:
        type_print(f"There were {green_diff} less green nests laid last year")
    elif green_diff == 0:
        type_print("The same amount of nests were laid last year")

    type_print("Calculating difference in loggerhead turtle nest numbers compared to last year")
    last_loggerhead = int(logger_20.acell('F3').value)
    this_loggerhead = int(info.acell('E2').value)
    loggerhead_diff = last_loggerhead - this_loggerhead
    if loggerhead_diff > 0:
        type_print(f"There were {loggerhead_diff} more loggerhead nests laid last year")
    elif loggerhead_diff < 0:
        type_print(f"There were {loggerhead_diff} less loggerhead nests laid last year")
    elif loggerhead_diff == 0:
        type_print("The same amount of nests were laid last year")


welcome()
collect_raw_data()
# total = calculate_total_nests()
# append_total_nests(total)
# calculate_data_logger_stock()
# calculate_green_and_logger_nests()
# calculate_difference()






# 01/06/2021,GREEN,CY1234,b1,y,y
# raw_data = SHEET.worksheet('raw_data')
# new_green = SHEET.worksheet('green_21')
# green_20 = SHEET.worksheet('green_20')
# new_logger = SHEET.worksheet('log_21')
# logger_20 = SHEET.worksheet('log_20')
# info = SHEET.worksheet('admin')
