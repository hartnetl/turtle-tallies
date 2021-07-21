import gspread
from google.oauth2.service_account import Credentials
# import sys
# import time
from termcolor import cprint
from datetime import datetime

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
raw_data = SHEET.worksheet('raw_data_21')
new_green = SHEET.worksheet('green_21')
green_20 = SHEET.worksheet('green_20')
new_logger = SHEET.worksheet('log_21')
logger_20 = SHEET.worksheet('log_20')
info = SHEET.worksheet('admin')

# define text colours
print_red = lambda x: cprint(x, 'red')
print_green = lambda x: cprint(x, 'green')
print_blue = lambda x: cprint(x, 'blue')


def welcome_title():
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

    user = input("Enter name: \n")
    print(
        f"Welcome {user}, if this is your first time entering data \
please ensure you have read the readme in the spreadsheet for detailed \
info. \n")


def welcome_msg():
    """
    Ask user if they would like to view or enter data.
    If they would like to enter data the program is run.
    If they want to view, a summary of data is shown and they're asked again
    if they would like to enter data.
    If yes, the program continues to run. If no, the program terminates.
    """
    start = input("Would you like to view or enter data? (VIEW/ENTER) \n")

    if start.upper() == "VIEW":
        summary()

        while True:
            keep_going = input("Would you like to enter data? (Y/N)\n")
            if validate_keep_going(keep_going):
                if keep_going.upper() == "Y":
                    print("You'd like to enter some data!\n")
                    collect_data()
                    break
                elif keep_going.upper() == "N":
                    print("You don't need to enter more data\n")
                    print("Goodbye! \n")
                    print("Press the button on top to start again")
                    exit()

    elif start.upper() == "ENTER":
        print()
        collect_data()

    else:
        print("You did not enter 'VIEW' or 'ENTER', try again")
        welcome_msg()


def validate_keep_going(keep_going):
    try:
        if keep_going.upper() != "Y" and keep_going.upper() != "N":
            raise ValueError(
                f"You must answer 'Y' or 'N', you answered {keep_going}")
    except ValueError as e:
        print(f"Invalid entry: {e}, try again")
        return False
    return True


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
# def help():
#     """
#     Provide help info for users if needed
#     """
#     print_green("HELP")
#     print_green('Headings:')
#     print_green("DATE, SPECIES, ID, LOCATION, NEST(Y/N), DATA LOGGER (Y/N)")
#     print_green("For 'DATE' enter the date the turtle or nest was observed in \
# format day/month/year")
#     print_green("For 'SPECIES', enter 'GREEN' for Green Sea Turtle or 'LOG' \
# for Loggerhead Turtle")
#     print_green("For 'ID' enter the id code on the turtle's flipper tag, which \
# is CY followed by 4 digits")
#     print_green("For 'LOCATION' enter B1 or B2 for the beach that you observed \
# the turtle or nest")
#     print_green("For 'NEST' type 'Y' if a nest was successfully laid, or 'N' \
# if the nest and egg laying was not completed")
#     print_green("For 'DATA LOGGER' type 'Y' if a data logger was placed in the \
# nest, and 'N' if it wasn't. Type NA if no nest was laid.")
#     print(" ")
#     print_green('Examples:')
#     print_green("01/06/2021, LOG, CY0000, B1, Y, Y")
#     print_green("01/06/2021, GREEN, CY0101, B2, N, NA\n")


# Functions below to collect and validate information from user
user_data = []


def get_date():
    """
    Ask user for the date and append it to user_data
    """
    while True:
        # print("Collecting date data")
        user_date = input("Enter the date (format: 01/06/21): \n ")

        if validate_date(user_date):
            # print("date was entered correctly")
            date_obj = datetime.strptime(user_date, "%d/%m/%y")
            if date_obj.day <= 7:
                user_data.append("Week 1")
                user_data.append(user_date)
                break
            elif date_obj.day <= 14:
                user_data.append("Week 2")
                user_data.append(user_date)
                break
            elif date_obj.day <= 21:
                user_data.append("Week 3")
                user_data.append(user_date)
                break
            elif date_obj.day <= 30:
                user_data.append("Final Week")
                user_data.append(user_date)
                break


def validate_date(user_date):
    """
    Validates that the date input is day/month/year.
    Throws an error if it is not and user will be asked to enter it again.
    """
    try:
        date_obj = datetime.strptime(user_date, "%d/%m/%y")
        if date_obj.month != 6:
            raise ValueError(
                f"The month should be '06', you entered '{date_obj.month}'")
        elif date_obj.year != 2021:
            raise ValueError(
                f"The year should be '2021', you entered '{date_obj.year}'")
    except ValueError as e:
        print(f"Invalid entry: {e}, try again")
        return False
    return True


def get_species():
    """
    Asks user for the species of turtle and sends input to validate input.
    The while loop will ask for the data until it is correctly entered.
    If it is validated it is added to user_data.
    """
    while True:
        # print("Collecting species data")
        species = input("Enter the species ('LOG' or 'GREEN'): \n ")

        if validate_species(species):
            # print("Species was entered correctly!")
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
        # print("Collecting turtle ID data")
        turtle = input("Enter the turtle ID (CY followed by 4 digits): \n ")

        if validate_turtle(turtle):
            # print("Turtle ID was entered correctly!")
            user_data.append(turtle)
            break


def validate_turtle(turtle):
    """
    Validates that the ID input is 6 characters long.
    Throws an error if it is not and user will be asked to enter it again.
    """
    try:
        # Come back and make this better, or remove letters
        if turtle[:2].upper() != "CY":
            raise ValueError(
                F"Turtle ID should be CY followed by 4 digits, you entered \
{turtle}")
        elif len(turtle) != 6:
            raise ValueError(
                f"ID should be 6 characters, you entered {len(turtle)}")
        elif not int(turtle[-4:].isdigit()):
            raise ValueError(
                f"ID should end in 4 digits, you entered {turtle[-4:]}")
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
        # print("Collecting beach ID data")
        beach = input("Enter the beach ID ('B1' or 'B2'): \n ")

        if validate_beach(beach):
            # print("Beach ID was entered correctly!")
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
        # print("Collecting nest data")
        nest = input("Was a nest laid (Y/N)?: \n ")

        if validate_nest(nest):
            # print("Nest data was entered correctly!")
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
    Asks user if a data logger was placed in the nest and sends input to
    validate input.
    The while loop will ask for the data until it is correctly entered.
    If it is validated it is added to user_data.
    """
    while True:
        # print("Collecting data logger data")
        data = input("Was a data logger placed in the nest (Y/N)?: \n ")

        if validate_data(data):
            # print("Data logger data was entered correctly!")
            user_data.append(data)
            break


def validate_data(data):
    """
    Validates that the input is Y or N.
    Throws an error if it is not and user will be asked to enter it again.
    """
    try:
        if data.upper() != "Y" and data.upper() != "N" and data.upper() != \
    "NA":
            raise ValueError(
                f"Enter 'Y', 'N' or 'NA', you entered {data}")
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
    After validation, the data input by the user is added to the raw data
    worksheet.
    """
    # print("Updating the worksheets\n")
    upper_data = [item.upper() for item in data]
    raw_data.append_row(upper_data)
    print("Raw datasheet update complete!\n")

    if upper_data[2] == "LOG":
        upper_data.remove('LOG')
        new_logger.append_row(upper_data)
        print("Loggerhead data also sent to log_21 worksheet \n")
    elif upper_data[2] == "GREEN":
        upper_data.remove('GREEN')
        new_green.append_row(upper_data)
        print("Green data also sent to green_21 worksheet \n")


def calculate_total_nests():
    """
    Counts the number of nests laid in raw data sheet
    """
    print("Calculating total nests \n")
    nest_col = raw_data.col_values(6)
    total = 0
    for item in nest_col:
        if item == "Y":
            total += 1
    return total


def calculate_nest_attempts():
    """
    Calculates the number of nests attempted, successful or not
    """
    print("Calculating nest attempts \n")
    nest_col = raw_data.col_values(6)
    attempts = 0
    for item in nest_col:
        if item == "Y" or item == "N":
            attempts += 1
    info.update('H2', attempts)
    # print("Returning total attempts")
    return attempts


def append_total_nests(total, attempts):
    """
    Updates the total nest value in admin worksheet and returns total to user
    """
    info.update('B2', total)
    updated = info.acell('B2').value
    print("Updating total nests laid in admin worksheet \n")


def calculate_green_and_logger_nests():
    """
    Calculates and returns how many nests have been laid by loggerhead
    and green turtles this season so far
    """
    # Calculate greens first
    green_nest = new_green.col_values(5)
    green_total = 0
    print("Calculating green nests \n")
    for item in green_nest:
        if item == "Y":
            green_total += 1

    # print("Adding to admin sheet")
    info.update('D2', green_total)
    green = info.acell('D2').value
#     print(f"There have been {green} Green Sea Turtle nests laid so far \
# this season")

    # Now the loggerheads
    logger_nest = new_logger.col_values(5)
    logger_total = 0
    print("Calculating logger nests \n")
    for items in logger_nest:
        if items == "Y":
            logger_total += 1

    # print("Adding to admin sheet")
    info.update('E2', logger_total)
    logger = info.acell('E2').value
#     print(f"There have been {logger} Loggerhead Turtle nests laid so far \
# this season")


def calculate_data_logger_stock():
    """
    Updates number of data loggers left and returns value to user
    """
    data_logs = raw_data.col_values(7)[-1]
    logs = info.acell('A2').value
    total = int(logs)
    if data_logs == "Y":
        total -= 1
    print("Calculating data loggers left \n")

    info.update("A2", total)
    print("Updating data log stock value")
    updated = info.acell('A2').value
    # print(f"You have {updated} data loggers left \n")


def calculate_nest_differences():
    """
    Calculate and return the number of nests laid compared to last year
    """
    print("Calculating difference in total nest numbers compared to last year \n")
    last_total = int(info.acell('C2').value)
    this_total = int(info.acell('B2').value)
    total_diff = last_total - this_total
    info.update('I2', total_diff)
    
    print("Calculating difference in green turtle nest numbers compared \
to last year \n")
    last_green = int(green_20.acell('G2').value)
    this_green = int(info.acell('D2').value)
    green_diff = last_green - this_green
    info.update('F2', green_diff)
   
    print("Calculating difference in loggerhead turtle nest numbers compared \
to last year \n")
    last_loggerhead = int(logger_20.acell('G2').value)
    this_loggerhead = int(info.acell('E2').value)
    loggerhead_diff = last_loggerhead - this_loggerhead
    info.update('G2', loggerhead_diff)
    return loggerhead_diff


def summary():
    """
    A summary of the calculations made by the program
    """
    print("Here is the summary of your data for this season \n")
    attempts = info.acell('H2').value
    total_laid = info.acell('B2').value
    green = info.acell('D2').value
    loggerhead = info.acell('E2').value
    loggers = info.acell('A2').value
    total_diff = int(info.acell('I2').value)
    green_diff = int(info.acell('F2').value)
    loggerhead_diff = int(info.acell('G2').value)

    print(
        f"Total nests attempted: {attempts} \n"
        f"Total nests laid: {total_laid} \n"
        f"Nests laid by green turtles: {green}\n"
        f"Nests laid by loggerhead turtles: {loggerhead} \n"
        f"Data loggers left: {loggers} \n ")

    if total_diff > 0:
        print(f"There were {total_diff} more nests laid in total last year \n")
    elif total_diff < 0:
        print(f"There were {total_diff} less nests laid in total last year \n")
    elif total_diff == 0:
        print("The same amount of nests were laid last year \n")

    if green_diff > 0:
        print(f"There was {green_diff} more green nests laid last year \n")
    elif green_diff < 0:
        green_diff_ = - (green_diff)
        print(f"There was {green_diff_} less green nests laid last year \n")
    elif green_diff == 0:
        print("The same amount of nests were laid last year \n")

    if loggerhead_diff > 0:
        print(f"There was {loggerhead_diff} more loggerhead nests laid \
last year \n")
    elif loggerhead_diff < 0:
        loggerhead_diff_ = - (loggerhead_diff)
        print(f"There was {loggerhead_diff_} less loggerhead nests laid \
 last year \n")
    elif loggerhead_diff == 0:
        print("The same amount of nests were laid last year \n")


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
    # print("Returning data")
    return user_data


def main(user_data):
    print()
    print("Sending data to worksheets \n")
    send_data_to_worksheets(user_data)
    total = calculate_total_nests()
    attempts = calculate_nest_attempts()
    append_total_nests(total, attempts)
    calculate_data_logger_stock()
    calculate_green_and_logger_nests()
    calculate_nest_differences()


welcome_title()
welcome_msg()
main(user_data)
summary()

# 01/06/2021,GREEN,CY1234,b1,y,y
# raw_data = SHEET.worksheet('raw_data')
# new_green = SHEET.worksheet('green_21')
# green_20 = SHEET.worksheet('green_20')
# new_logger = SHEET.worksheet('log_21')
# logger_20 = SHEET.worksheet('log_20')
# info = SHEET.worksheet('admin')
