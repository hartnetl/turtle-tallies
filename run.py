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
raw_20 = SHEET.worksheet('raw_data_20')
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
    print_green("""
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

    user = input("Enter name: \n")
    print_blue(
        f"Welcome {user}, if this is your first time entering data \
please ensure you have \nread the readme in the spreadsheet for detailed \
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
                    print_green("You'd like to enter some data!\n")
                    collect_data()
                    break
                elif keep_going.upper() == "N":
                    print_blue("You don't need to enter more data\n")
                    print_blue("Goodbye! \n")
                    print_red("Press the button on top to start again")
                    exit()

    elif start.upper() == "ENTER":
        print()
        collect_data()

    else:
        print_red("You did not enter 'VIEW' or 'ENTER', try again \n")
        welcome_msg()


def validate_keep_going(keep_going):
    try:
        if keep_going.upper() != "Y" and keep_going.upper() != "N":
            raise ValueError(
                f"You must answer 'Y' or 'N', you answered {keep_going}")
    except ValueError as e:
        print_red(f"Invalid entry: {e}, try again \n")
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


# Functions below to collect and validate information from user
user_data = []


def get_date():
    """
    Ask user for the date and append it to user_data
    """
    while True:
        user_date = input("Enter the date (format: 01/06/21): \n ")

        if validate_date(user_date):
            date_obj = datetime.strptime(user_date, "%d/%m/%y")
            if date_obj.day <= 7:
                user_data.append("WEEK1")
                user_data.append(user_date)
                break
            elif date_obj.day <= 14:
                user_data.append("WEEK2")
                user_data.append(user_date)
                break
            elif date_obj.day <= 21:
                user_data.append("WEEK3")
                user_data.append(user_date)
                break
            elif date_obj.day <= 30:
                user_data.append("FINALWEEK")
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
        print_red(f"Invalid entry: {e}, try again \n")
        return False
    return True


def get_species():
    """
    Asks user for the species of turtle and sends input to validate input.
    The while loop will ask for the data until it is correctly entered.
    If it is validated it is added to user_data.
    """
    while True:
        species = input("Enter the species ('LOG' or 'GREEN'): \n ")

        if validate_species(species):
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
        print_red(f"Invalid entry: {e}, try again \n")
        return False
    return True


def get_turtle_id():
    """
    Asks user for the turtle ID  and sends input to validate input.
    The while loop will ask for the data until it is correctly entered.
    If it is validated it is added to user_data.
    """
    while True:
        turtle = input("Enter the turtle ID (CY followed by 4 digits): \n ")

        if validate_turtle(turtle):
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
        print_red(f"Invalid entry: {e}, try again \n")
        return False
    return True


def get_beach_id():
    """
    Asks user for the beach ID and sends input to validate input.
    The while loop will ask for the data until it is correctly entered.
    If it is validated it is added to user_data.
    """
    while True:
        beach = input("Enter the beach ID ('B1' or 'B2'): \n ")

        if validate_beach(beach):
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
        print_red(f"Invalid entry: {e}, try again \n")
        return False
    return True


def get_nest_info():
    """
    Asks user if a nest was laid and sends input to validate input.
    The while loop will ask for the data until it is correctly entered.
    If it is validated it is added to user_data.
    """
    while True:
        nest = input("Was a nest laid (Y/N)?: \n ")

        if validate_nest(nest):
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
        print_red(f"Invalid entry: {e}, try again \n")
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
        data = input("Was a data logger placed in the nest (Y/N)?: \n ")

        if validate_data(data):
            user_data.append(data)
            break


def validate_data(data):
    """
    Validates that the input is Y or N.
    Throws an error if it is not and user will be asked to enter it again.
    """
    try:
        if data.upper() != "Y" and data.upper() != "N" \
         and data.upper() != "NA":
            raise ValueError(
                f"Enter 'Y', 'N' or 'NA', you entered {data}")
    except ValueError as e:
        print_red(f"Invalid entry: {e}, try again \n")
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
    elif letter.upper() == "N":
        print_red("Please enter the information again \n")
        collect_data()
    else:
        print_red("You must enter 'Y' or 'N' \n")
        letter = input("Is the information you input correct? Y/N \n")
        user_verifiy_input(letter)


# == End of collecting data ==


def send_data_to_worksheets(data):
    """
    After validation, the data input by the user is added to the raw data
    worksheet.
    """
    print_blue("Updating the worksheets\n")
    upper_data = [item.upper() for item in data]
    raw_data.append_row(upper_data)

    print_blue("Updating weekly tally for raw data sheet \n")

    if upper_data[0] == "WEEK1" and upper_data[5] == "Y":
        raw_w1 = int(raw_data.acell('H2').value)
        print_blue("adding 1 to week 1 nest tally \n")
        raw_w1 += 1
        raw_data.update('H2', raw_w1)
    elif upper_data[0] == "WEEK2" and upper_data[5] == "Y":
        raw_w2 = int(raw_data.acell('H3').value)
        print_blue("adding 1 to week 2 nest tally \n")
        raw_w2 += 1
        raw_data.update('H3', raw_w2)
    elif upper_data[0] == "WEEK3" and upper_data[5] == "Y":
        raw_w3 = int(raw_data.acell('H4').value)
        print_blue("adding 1 to week 3 nest tally \n")
        raw_w3 += 1
        raw_data.update('H4', raw_w3)
    elif upper_data[0] == "FINALWEEK" and upper_data[5] == "Y":
        raw_wF = int(raw_data.acell('H5').value)
        print_blue("adding 1 to final week nest tally \n")
        raw_wF += 1
        raw_data.update('H5', raw_wF)

    print_blue("Raw datasheet update complete\n")

    if upper_data[2] == "LOG":
        print_blue("Sending data to Loggerhead worksheet \n")
        upper_data.remove('LOG')
        new_logger.append_row(upper_data)
        print_blue("Loggerhead data sent to log_21 worksheet \n")
        print_blue("Calculating new tally \n")

        if upper_data[0] == "WEEK1" and upper_data[5] == "Y":
            log_w1 = int(new_logger.acell('G2').value)
            print_blue("adding 1 to week 1 nest tally \n")
            log_w1 += 1
            new_logger.update('G2', log_w1)
        elif upper_data[0] == "WEEK2" and upper_data[5] == "Y":
            log_w2 = int(new_logger.acell('G3').value)
            print_blue("adding 1 to week 2 nest tally \n")
            log_w2 += 1
            new_logger.update('G3', log_w2)
        elif upper_data[0] == "WEEK3" and upper_data[5] == "Y":
            log_w3 = int(new_logger.acell('G4').value)
            print_blue("adding 1 to week 3 nest tally \n")
            log_w3 += 1
            new_logger.update('G4', log_w3)
        elif upper_data[0] == "FINALWEEK" and upper_data[5] == "Y":
            log_wF = int(new_logger.acell('G5').value)
            print_blue("adding 1 to final week nest tally \n")
            log_wF += 1
            new_logger.update('G5', log_wF)

    elif upper_data[2] == "GREEN":
        print_blue("Sending data to Green worksheet \n")
        upper_data.remove('GREEN')
        new_green.append_row(upper_data)
        print_blue("Green data also sent to green_21 worksheet \n")
        print_blue("Calculating new tally \n")

        if upper_data[0] == "WEEK1" and upper_data[5] == "Y":
            green_w1 = int(new_green.acell('G2').value)
            print_blue("adding 1 to week 1 nest tally \n")
            green_w1 += 1
            new_green.update('G2', green_w1)
        elif upper_data[0] == "WEEK2" and upper_data[5] == "Y":
            green_w2 = int(new_green.acell('G3').value)
            print_blue("adding 1 to week 2 nest tally \n")
            green_w2 += 1
            new_green.update('G3', green_w2)
        elif upper_data[0] == "WEEK3" and upper_data[5] == "Y":
            green_w3 = int(new_green.acell('G4').value)
            print_blue("adding 1 to week 3 nest tally \n")
            green_w3 += 1
            new_green.update('G4', green_w3)
        elif upper_data[0] == "FINALWEEK" and upper_data[5] == "Y":
            green_wF = int(new_green.acell('G5').value)
            print_blue("adding 1 to final week nest tally \n")
            green_wF += 1
            new_green.update('G5', green_wF)


def calculate_total_nests():
    """
    Counts the number of nests laid in raw data sheet
    """
    print_blue("Calculating total nests \n")
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
    print_blue("Calculating nest attempts \n")
    nest_col = raw_data.col_values(6)
    attempts = 0
    for item in nest_col:
        if item == "Y" or item == "N":
            attempts += 1
    info.update('H2', attempts)
    return attempts


def append_total_nests(total, attempts):
    """
    Updates the total nest value in admin worksheet and returns total to user
    """
    print_blue("Updating total nests laid in admin worksheet \n")
    info.update('B2', total)
    # updated = info.acell('B2').value


def calculate_green_and_logger_nests():
    """
    Calculates and returns how many nests have been laid by loggerhead
    and green turtles this season so far
    """
    # Calculate number of Green turtle nests
    green_nest = new_green.col_values(5)
    green_total = 0
    print_blue("Calculating green nests \n")
    for item in green_nest:
        if item == "Y":
            green_total += 1

    # Append total to info worksheet
    print_blue("Adding green nest total to admin sheet \n")
    info.update('D2', green_total)

    # Calculate number of Loggerhead turtle nests
    logger_nest = new_logger.col_values(5)
    logger_total = 0
    print_blue("Calculating logger nests \n")
    for items in logger_nest:
        if items == "Y":
            logger_total += 1

    print_blue("Adding Loggerhead total nests to admin sheet \n")
    info.update('E2', logger_total)


def calculate_data_logger_stock():
    """
    Updates number of data loggers left and returns value to user
    """
    print_blue("Calculating how many data loggers are left \n")
    data_logs = raw_data.col_values(7)[-1]
    logs = info.acell('A2').value
    total = int(logs)
    if data_logs == "Y":
        total -= 1

    print_blue("Updating data log stock value  \n")
    info.update("A2", total)
    log_count = int(info.acell('A2').value)
    if log_count < 20:
        print_red(f"You have {log_count} data loggers left. Order more.")





def calculate_nest_differences():
    """
    Calculate and return the number of nests laid compared to last year
    """
    print_blue("Calculating difference in total nest numbers compared to \
last year \n")
    last_total = int(info.acell('C2').value)
    this_total = int(info.acell('B2').value)
    total_diff = last_total - this_total
    info.update('I2', total_diff)

    print_blue("Calculating difference in green turtle nest numbers compared \
to last year \n")
    last_green = int(green_20.acell('G2').value)
    this_green = int(info.acell('D2').value)
    green_diff = last_green - this_green
    info.update('F2', green_diff)

    print_blue("Calculating difference in loggerhead turtle nest numbers compared \
to last year \n")
    last_loggerhead = int(logger_20.acell('G2').value)
    this_loggerhead = int(info.acell('E2').value)
    loggerhead_diff = last_loggerhead - this_loggerhead
    info.update('G2', loggerhead_diff)
    return loggerhead_diff


def compare_weeks(week):
    print_blue("Preparing weekly comparisons")
    total_week_1 = int(raw_data.acell('H2').value)
    last_total_week_1 = int(raw_20.acell('H2').value)
    green_week_1 = int(new_green.acell('G2').value)
    last_green_week_1 = int(green_20.acell('H2').value)
    loggerhead_week_1 = int(new_logger.acell('G2').value)
    last_loggerhead_week_1 = int(logger_20.acell('H2').value)

    total_week_2 = int(raw_data.acell('H3').value)
    last_total_week_2 = int(raw_20.acell('H3').value)
    green_week_2 = int(new_green.acell('G3').value)
    last_green_week_2 = int(green_20.acell('H3').value)
    loggerhead_week_2 = int(new_logger.acell('G3').value)
    last_loggerhead_week_2 = int(logger_20.acell('H3').value)

    total_week_3 = int(raw_data.acell('H4').value)
    last_total_week_3 = int(raw_20.acell('H4').value)
    green_week_3 = int(new_green.acell('G4').value)
    last_green_week_3 = int(green_20.acell('H4').value)
    loggerhead_week_3 = int(new_logger.acell('G4').value)
    last_loggerhead_week_3 = int(logger_20.acell('H4').value)

    total_week_final = int(raw_data.acell('H5').value)
    last_total_week_final = int(raw_20.acell('H5').value)
    green_week_final = int(new_green.acell('G5').value)
    last_green_week_final = int(green_20.acell('H5').value)
    loggerhead_week_final = int(new_logger.acell('G5').value)
    last_loggerhead_week_final = int(logger_20.acell('H4').value)

    if week == '1':
        print_green(
            f"In the first week of the season {total_week_1} nests have been \
laid, in comparison to {last_total_week_1} last year. \n {green_week_1} of \
these were laid by Green turtles, while {last_green_week_1} were laid by \
Greens this time last year. \n Loggerheads laid {loggerhead_week_1} nests in \
the first week and {last_loggerhead_week_1} were laid by them during this same\
period last year. \n")

    elif week == '2':
        print_green(
            f"In the second week of the season {total_week_2} nests have been \
laid, in comparison to {last_total_week_2} last year. \n {green_week_2} of \
these were laid by Greens, while {last_green_week_2} were laid by Greens this \
time last year. \n Loggerheads laid {loggerhead_week_2} nests in the first \
week, and {last_loggerhead_week_2} were laid by them during this same \
period last year.\n")

    elif week == '3':
        print_green(
            f"In the third week of the season {total_week_3} nests have been \
laid, in comparison to {last_total_week_3} last year. \n{green_week_3} of \
these were laid by Greens, while {last_green_week_3} were laid by Greens this \
time last year. \nLoggerheads laid {loggerhead_week_3} nests in the first \
week, and {last_loggerhead_week_3} were laid by them during this same \
period last year.\n")

    elif week.lower() == 'last':
        print_green(
             f"In the final week of the season {total_week_final} nests have \
been laid, in comparison to {last_total_week_final} last year. \n \
{green_week_final} of these were laid by green, while {last_green_week_final} \
were laid by Greens this time last year. \nLoggerheads laid \
{loggerhead_week_final} nests in the first week, and \
{last_loggerhead_week_final} were laid by them during this same \
period last year.\n")


def summary():
    """
    A summary of the calculations made by the program
    """
    print_green("Here is the summary of your data for this season: \n")
    attempts = info.acell('H2').value
    total_laid = info.acell('B2').value
    green = info.acell('D2').value
    loggerhead = info.acell('E2').value
    loggers = info.acell('A2').value
    total_diff = int(info.acell('I2').value)
    green_diff = int(info.acell('F2').value)
    loggerhead_diff = int(info.acell('G2').value)

    print_green(
        f"Total nests attempted: {attempts} \n"
        f"Total nests laid: {total_laid} \n"
        f"Nests laid by green turtles: {green}\n"
        f"Nests laid by loggerhead turtles: {loggerhead} \n"
        f"Data loggers left: {loggers} \n ")

    if total_diff > 0:
        print_green(f"There were {total_diff} more nests laid in total \
last year \n")
    elif total_diff < 0:
        total_diff_ = - (total_diff)
        print_green(f"There were {total_diff_} less nests laid in total \
last year \n")
    elif total_diff == 0:
        print_green("The same amount of nests were laid last year \n")

    if green_diff > 0:
        print_green(f"There was {green_diff} more Green nests laid last \
year \n")
    elif green_diff < 0:
        green_diff_ = - (green_diff)
        print_green(f"There was {green_diff_} less Green nests laid last \
year \n")
    elif green_diff == 0:
        print_green("The same amount of nests were laid by Green turtles last \
year \n")

    if loggerhead_diff > 0:
        print_green(f"There was {loggerhead_diff} more Loggerhead nests laid \
last year \n")
    elif loggerhead_diff < 0:
        loggerhead_diff_ = - (loggerhead_diff)
        print_green(f"There was {loggerhead_diff_} less Loggerhead nests laid \
last year \n")
    elif loggerhead_diff == 0:
        print_green("The same amount of nests were laid by Loggerheads last \
year \n")


def compare_q():
    final_compare = input("Would you like to see a comparison of weekly nest \
abundance? (Y/N) \n")
    if final_compare.upper() == "N":
        print_blue("You're all done. Goodbye! \n")
        print_red("Press the button on top to restart the program.")
        exit()
    elif final_compare.upper() == "Y":
        compare()
    else: 
        print_red(f"You entered {final_compare}, please enter Y or N \n")
        compare_q()


def compare():
    while True:
        week = input("Choose your week to compare: 1 , 2, 3, or last. Type \
'quit' to exit \n")
        if validate_week(week):
            print_blue(f"You have chosen: {week}")
            compare_weeks(week)
            repeat = input("Would you like to compare another week?  \n")
            if validate_keep_going(repeat):
                if repeat.upper() == "Y":
                    compare()
                elif repeat.upper == "N":
                    print_blue("You're all done \n")
                    print_red("Click the top button to restart the program")


def validate_week(week):
    try:
        if week != '1' and week != '2' and week != '3' and  \
week.upper() != 'LAST' and week.upper() != "QUIT":
            raise ValueError(
                f"You must enter 1, 2, 3, or last. You entered {week}")
        elif week.upper() == "QUIT":
            print_blue("You chose to exit the program. Now closing.")
            print_red("Press the top button to run the program again.")
            exit()
    except ValueError as e:
        print_red(f"Invalid response: {e}, try again")
        return False
    return True


compare_q()


def more_input():
    more = input("Do you have more data to enter? (Y/N) \n ")
    if more.upper() == "Y":
        collect_data()
    elif more.upper() == "N":
        pass
    else:
        print_red("You have entered an invalid response. Please enter 'Y' or \
'N' \n")
        more_input()


def collect_data():
    get_date()
    get_species()
    get_turtle_id()
    get_beach_id()
    get_nest_info()
    get_data_logger_info()

    print_blue(f"The data you have entered is {user_data}")
    check = input("Is this correct? (Y/N): \n")
    user_verifiy_input(check)
    return user_data


def main(user_data):
    print()
    print_blue("Sending data to worksheets \n")
    send_data_to_worksheets(user_data)
    total = calculate_total_nests()
    attempts = calculate_nest_attempts()
    append_total_nests(total, attempts)
    calculate_data_logger_stock()
    calculate_green_and_logger_nests()
    calculate_nest_differences()
    more_input()


# welcome_title()
# welcome_msg()
# main(user_data)
# summary()
# compare_q()
