import gspread
from google.oauth2.service_account import Credentials
import sys
import time
from termcolor import cprint

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

# define text colours
print_red = lambda x: cprint(x, 'red')
print_green = lambda x: cprint(x, 'green')
print_blue = lambda x: cprint(x, 'blue')


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
                ╩ ╚═╝╩╚═ ╩ ╩═╝╚═╝   ╩ ╩ ╩╩═╝╩═╝╩╚═╝╚═╝..
    """)


# Credit for help with this function
# https://stackoverflow.com/questions/4099422/printing-slowly-simulate-typing
# def type_print(str):
#     """
#     Prints text out letter by letter instead of all at once
#     """
#     for letter in str + '\n':
#         sys.stdout.write(letter)
#         sys.stdout.flush()
#         time.sleep(.1)


# def fast_print(str):
#     """
#     Prints text out quickly letter by letter instead of all at once
#     """
#     for letter in str + '\n':
#         sys.stdout.write(letter)
#         sys.stdout.flush()
#         time.sleep(.01)


# Help message for formatting the correct input
def help():
    """
    Provide help info for users if needed
    """
    print_green("HELP")
    print_green('Headings:')
    print_green("DATE, SPECIES, ID, LOCATION, NEST(Y/N), DATA LOGGER (Y/N)")
    print_green("For 'DATE' enter the date the turtle or nest was observed in format day/month/year")
    print_green("For 'SPECIES', enter 'GREEN' for Green Sea Turtle or 'LOG' for Loggerhead Turtle")
    print_green("For 'ID' enter the id code on the turtle's flipper tag, which is CY followed by 4 digits")
    print_green("For 'LOCATION' enter B1 or B2 for the beach that you observed the turtle or nest")
    print_green("For 'NEST' type 'Y' if a nest was successfully laid, or 'N' if the nest and egg laying was not completed")
    print_green("For 'DATA LOGGER' type 'Y' if a data logger was placed in the nest, and 'N' if it wasn't. Type NA if no nest was laid.")
    print(" ")
    print_green('Examples:')
    print_green("01/06/2021, LOG, CY0000, B1, Y, Y")
    print_green("01/06/2021, GREEN, CY0101, B2, N, NA\n")


# Functions below to collect and validate information from user
user_data = []


def get_date():
    """
    Ask user for the date and append it to user_data
    """
    print("Collecting date data")
    date = input("Enter the date (format: 1/6/21): \n ")
    user_data.append(date)


def get_species():
    """
    Asks user for the species of turtle and sends input to validate input.
    The while loop will ask for the data until it is correctly entered.
    If it is validated it is added to user_data.
    """
    while True: 
        print("Collecting species data")
        species = input("Enter the species ('LOG' or 'GREEN'): \n ")

        if validate_species(species):
            print("Species was entered correctly!")
            user_data.append(species)
            break


def validate_species(species):
    """
    Validates that the species input is "LOG" or "GREEN".
    Throws an error if it is not and user will be asked to enter it again.
    """
    try:
        if species.upper() != "LOG" and species.upper() != "GREEN":
            raise ValueError(
                F"Species should be 'GREEN' or 'LOG', you entered {species}")
    except ValueError as e:
        print(f"Invalid entry: {e}, try again")
        return False
    return True


def get_turtle_id():
    """
    Asks user for the turtle ID  and sends input to validate input.
    The while loop will ask for the data until it is correctly entered.
    If it is validated it is added to user_data.
    """
    while True: 
        print("Collecting turtle ID data")
        turtle = input("Enter the turtle ID (CY followed by 4 digits): \n ")

        if validate_turtle(turtle):
            print("Turtle ID was entered correctly!")
            user_data.append(turtle)
            break


def validate_turtle(turtle):
    """
    Validates that the ID input is 6 characters long.
    Throws an error if it is not and user will be asked to enter it again.
    """
    try:
        # Come back and make this better, or remove letters
        if len(turtle) != 6:
            raise ValueError(
                F"Turtle ID should be CY followed by 4 digits, you entered {turtle}")
    except ValueError as e:
        print(f"Invalid entry: {e}, try again")
        return False
    return True


def get_beach_id():
    """
    Asks user for the beach ID and sends input to validate input.
    The while loop will ask for the data until it is correctly entered.
    If it is validated it is added to user_data.
    """
    while True:
        print("Collecting beach ID data")
        beach = input("Enter the beach ID ('B1' or 'B2'): \n ")

        if validate_beach(beach):
            print("Beach ID was entered correctly!")
            user_data.append(beach)
            break


def validate_beach(beach):
    """
    Validates that the beach ID input is B1 or B2.
    Throws an error if it is not and user will be asked to enter it again.
    """
    try:
        if beach.upper() != "B1" and beach.upper() != "B2":
            raise ValueError(
                F"Beach ID should be 'B1' or 'B2', you entered {beach}")
    except ValueError as e:
        print(f"Invalid entry: {e}, try again")
        return False
    return True


def get_nest_info():
    """
    Asks user if a nest was laid and sends input to validate input.
    The while loop will ask for the data until it is correctly entered.
    If it is validated it is added to user_data.
    """
    while True: 
        print("Collecting nest data")
        nest = input("Was a nest laid (Y/N)?: \n ")

        if validate_nest(nest):
            print("Nest data was entered correctly!")
            user_data.append(nest)
            break


def validate_nest(nest):
    """
    Validates that the input is Y or N.
    Throws an error if it is not and user will be asked to enter it again.
    """
    try:
        if nest.upper() != "Y" and nest.upper() != "N":
            raise ValueError(
                F"Enter 'Y' or 'N', you entered {nest}")
    except ValueError as e:
        print(f"Invalid entry: {e}, try again")
        return False
    return True


def get_data_logger_info():
    """
    Asks user if a data logger was placed in the nest and sends input to validate input.
    The while loop will ask for the data until it is correctly entered.
    If it is validated it is added to user_data.
    """
    while True: 
        print("Collecting data logger data")
        data = input("Was a data logger placed in the nest (Y/N)?: \n ")

        if validate_data(data):
            print("Data logger data was entered correctly!")
            user_data.append(data)
            break


def validate_data(data):
    """
    Validates that the input is Y or N.
    Throws an error if it is not and user will be asked to enter it again.
    """
    try:
        if data.upper() != "Y" and data.upper() != "N" and data.upper() != "NA":
            raise ValueError(
                F"Enter 'Y' or 'N', you entered {data}")
    except ValueError as e:
        print(f"Invalid entry: {e}, try again")
        return False
    return True


def user_verifiy_input(letter):
    """
    This checks if the user is sure they have entered the correct data.
    If yes, the program continues.
    If no, it asks for all the data to be entered again.
    """
    if letter.upper() == "Y":
        pass
    else:
        print_red("Try again\n")
        collect_data()


# == End of collecting data ==


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
        print("Loggerhead data also sent to log_21 worksheet")
    elif upper_data[1] == "GREEN":
        upper_data.remove('GREEN')
        new_green.append_row(upper_data)
        print("Green data also sent to green_21 worksheet")


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
    Calculates and returns how many nests have been laid by loggerhead
    and green turtles this season so far
    """
    # Calculate greens first
    green_nest = new_green.col_values(4)
    green_total = 0
    print("Calculating green nests")
    for item in green_nest:
        if item == "Y":
            green_total += 1

    print("Adding to admin sheet")
    info.update('D2', green_total)
    green = info.acell('D2').value
    print(f"There have been {green} Green Sea Turtle nests laid so far this season")

    # Now the loggerheads
    logger_nest = new_logger.col_values(4)
    logger_total = 0
    print("Calculating logger nests")
    for items in logger_nest:
        if items == "Y":
            logger_total += 1

    print("Adding to admin sheet")
    info.update('E2', logger_total)
    logger = info.acell('E2').value
    print(f"There have been {logger} Loggerhead Turtle nests laid so far this season")


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


def calculate_difference():
    """
    Calculate and return the number of green and
    logger turtle nests laid compared to last year
    """
    print("Calculating difference in total nest numbers compared to last year")
    last_total = int(info.acell('C2').value)
    this_total = int(info.acell('B2').value)
    total_diff = last_total - this_total
    if total_diff > 0:
        print(f"There were {total_diff} more nests laid in total last year")
    elif total_diff < 0:
        print(f"There were {total_diff} less nests laid in total last year")
    elif total_diff == 0:
        print("The same amount of nests were laid last year")

    print("Calculating difference in green turtle nest numbers compared to last year")
    last_green = int(green_20.acell('F2').value)
    this_green = int(info.acell('D2').value)
    green_diff = last_green - this_green
    if green_diff > 0:
        print(f"There were {green_diff} more green nests laid last year")
    elif green_diff < 0:
        print(f"There were {green_diff} less green nests laid last year")
    elif green_diff == 0:
        print("The same amount of nests were laid last year")

    print("Calculating difference in loggerhead turtle nest numbers compared to last year")
    last_loggerhead = int(logger_20.acell('F3').value)
    this_loggerhead = int(info.acell('E2').value)
    loggerhead_diff = last_loggerhead - this_loggerhead
    if loggerhead_diff > 0:
        print(f"There were {loggerhead_diff} more loggerhead nests laid last year")
    elif loggerhead_diff < 0:
        print(f"There were {loggerhead_diff} less loggerhead nests laid last year")
    elif loggerhead_diff == 0:
        print("The same amount of nests were laid last year")


# welcome()

def collect_data():
    get_date()
    get_species()
    get_turtle_id()
    get_beach_id()
    get_nest_info()
    get_data_logger_info()

    print(f"The data you have entered is {user_data}")
    check = input("Is this correct? (Y/N): \n")
    user_verifiy_input(check)
    print("Returning data")
    return user_data


def main(user_data):
    send_data_to_worksheets(user_data)
    # total = calculate_total_nests()
    # append_total_nests(total)
    # calculate_data_logger_stock()
    # calculate_green_and_logger_nests()
    # calculate_difference()


collect_data()
main(user_data)

# 01/06/2021,GREEN,CY1234,b1,y,y
# raw_data = SHEET.worksheet('raw_data')
# new_green = SHEET.worksheet('green_21')
# green_20 = SHEET.worksheet('green_20')
# new_logger = SHEET.worksheet('log_21')
# logger_20 = SHEET.worksheet('log_20')
# info = SHEET.worksheet('admin')
