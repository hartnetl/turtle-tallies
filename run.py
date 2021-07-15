import gspread
from google.oauth2.service_account import Credentials
import timg

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


def welcome():
    # print("""
    # ______________________________________██████████████████████____________________________
    # ________________________________████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓▓████████______________________
    # __________________________██████▓▓▓▓▓▓██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓▓▓▓▓▓████____________________
    # ______████████████______████▓▓▓▓▓▓████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████▓▓██████________________
    # ____██____________████████████▓▓▓▓████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████▓▓▓▓▓▓██▓▓▓▓████______________
    # __██____██__________██__██▓▓██████▓▓████████▓▓▓▓▓▓██████▓▓██▓▓▓▓▓▓████▓▓████____________
    # ██______██______________████▓▓▓▓██▓▓▓▓▓▓▓▓██████████▓▓▓▓▓▓▓▓██████▓▓▓▓██▓▓██████████____
    # ████______________██______████▓▓████▓▓▓▓████▓▓▓▓▓▓██▓▓▓▓████▓▓▓▓██▓▓▓▓▓▓██__________████
    # ____██████████████████______████▓▓████████▓▓▓▓▓▓▓▓██████▓▓▓▓▓▓▓▓▓▓████████____________██
    # ____________________████______██▓▓▓▓▓▓████████████▓▓▓▓██▓▓▓▓████████████____________██__
    # ______________________██████____██████████▓▓▓▓▓▓██▓▓▓▓▓▓██████________██████████████____
    # ________________________██████____████__██████████████████__████______██________________
    # ________________________██____██______████______________________████████________________
    # ________________________██____██________████████________________________________________
    # ________________________████____██____________████______________________________________
    # __________________________██____██______________████____________________________________
    # __________________________████____████____________████__________________________________
    # ____________________________██__██____██____________████________________________________
    # ____________________________██████______████__________██________________________________
    # ____________________________________________████████████________________________________
    # """)

    print("""
                                        ██████████████████████                            
                                    ████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓▓████████                      
                               ██████▓▓▓▓▓▓██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓▓▓▓▓▓████                    
          ████████████      ████▓▓▓▓▓▓████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████▓▓██████                
        ██            ████████████▓▓▓▓████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████▓▓▓▓▓▓██▓▓▓▓████              
      ██    ██          ██  ██▓▓██████▓▓████████▓▓▓▓▓▓██████▓▓██▓▓▓▓▓▓████▓▓████            
    ██      ██              ████▓▓▓▓██▓▓▓▓▓▓▓▓██████████▓▓▓▓▓▓▓▓██████▓▓▓▓██▓▓██████████    
    ████              ██      ████▓▓████▓▓▓▓████▓▓▓▓▓▓██▓▓▓▓████▓▓▓▓██▓▓▓▓▓▓██          ████
        ██████████████████      ████▓▓████████▓▓▓▓▓▓▓▓██████▓▓▓▓▓▓▓▓▓▓████████            ██
                        ████      ██▓▓▓▓▓▓████████████▓▓▓▓██▓▓▓▓████████████            ██  
                          ██████    ██████████▓▓▓▓▓▓██▓▓▓▓▓▓██████        ██████████████    
                            ██████    ████  ██████████████████  ████      ██                
                            ██    ██      ████                      ████████                
                            ██    ██        ████████                                        
                            ████    ██            ████                                      
                              ██    ██              ████                                    
                              ████    ████            ████                                  
                                ██  ██    ██            ████                                
                                ██████      ████          ██                                
                                                ████████████                    
    """)

    print("""
      _______  _    _  _____  _______  _       ______   _______         _       _       _____  ______   _____ 
     |__   __|| |  | ||  __ \|__   __|| |     |  ____| |__   __| /\    | |     | |     |_   _||  ____| / ____|
        | |   | |  | || |__) |  | |   | |     | |__       | |   /  \   | |     | |       | |  | |__   | (___  
        | |   | |  | ||  _  /   | |   | |     |  __|      | |  / /\ \  | |     | |       | |  |  __|   \___ \ 
        | |   | |__| || | \ \   | |   | |____ | |____     | | / ____ \ | |____ | |____  _| |_ | |____  ____) |
        |_|    \____/ |_|  \_\  |_|   |______||______|    |_|/_/    \_\|______||______||_____||______||_____/ 
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
    User inputs the collected raw data and it is added to the raw data worksheet.
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
    if letter == "Y" or letter == "y":
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
            raise ValueError(
                f"You must fill in all 6 fields, you only entered {len(userDataList)}"
            )
    except ValueError as e:
        print(f"Something went wrong: {e}, try again \n")


welcome()
# collect_raw_data()
