import datetime
import os, sys

def get_date_from_filename(file):
    """
    Filters out the numeric part of the file name
    and returns date in YYYY-mm-dd format.
    """
    date = "".join(filter(str.isdigit, file))
    date = date[:8]
    date = date[:4] + '-' + date[4:6] + '-' + date[6:]
    
    return(date)

def select_date():
    """
    Allows user to enter and return a date or defaults to current date.
    Checks for valid date entered.
    """
    current_date = datetime.datetime.today().strftime("%Y-%m-%d")

    date = input(f"Enter a date in format (YYYY-mm-dd) or press ENTER for today's date ({current_date}) \n")
    if not date:
        date = current_date

    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except:
        print("Error: Incorrect date format.")
        return select_date()

    return(date)

def get_files():
    """
    Checks the content of folder for .txt or .rtf files.
    Compares the date part of the filename against
    the selected date. Returns a list of files or 
    an error message if list is empty. 
    """
    files = []
    cwd = os.getcwd()

    for file in os.listdir(cwd):
        if file.endswith(".txt") or file.endswith(".rtf"):
            date = get_date_from_filename(file)
            if date == date_picked:
                files.append(file)

    if len(files) == 0:
        print("Folder does not contain files with the selected date.")
        input()
        sys.exit()

    return(files)


def process_files(files):
    """
    Iterates over lines in the file, counts chips created and error messages.
    If consecutive errors occur it counts the first one and ignores until a
    new chip appears.
    """
    chips = 0
    errors = 0
    for file in files:
        with open(file) as f:
            previous_line = ""
            for line in f.readlines():
                if line[0].isdigit():
                    previous_line = line
                    chips += 1
                elif line[0].isalpha() and not previous_line[0].isalpha():
                    errors += 1
                    previous_line = line
                    message = line.split("-")[1].strip()
                    if message in error_messages:
                        error_messages[message] += 1
                    else:
                        error_messages[message] = 1
    
    return(chips, errors)

def print_report():
    """
    Prints the summary of the file(s) for the selected date
    in a readable format.
    """
    print(f"\n\nDate:                                 {date_picked}")
    print(f"Number of chips created:              {chips}")
    print(f"Average errors per 10,000 chips:      {errors_average:.2f}") # errors_average with 2 decimal places
    print("-" * 80)
    print("Error" + (' ' * 60) + "Number of errors")
    print("\n")
    for key, value in error_messages.items():
        spaces = 80 - len(key)
        print(key + (' ' * spaces) + str(value))
    input()


date_picked = select_date()
files = get_files()
error_messages = {}
chips,errors = process_files(files)
errors_average = errors / chips * 10000 #average errors per 10,000 chips

print_report()

