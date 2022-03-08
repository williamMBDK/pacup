import os

colorcodes = {
    "header" : '\033[95m',
    "blue" : '\033[94m',
    "cyan" : '\033[96m',
    "green" : '\033[92m',
    "yellow" : '\033[93m',
    "red" : '\033[91m',
    "bold" : '\033[1m',
    "underline" : '\033[4m',
    "reset" : '\033[0m'
}

def colored(text, color):
    return "{}{}{}".format(colorcodes[color], text, colorcodes["reset"])

class PacupUserError(Exception):
    pass

class PacupInstallError(Exception):
    pass

class PacupUnknownError(Exception):
    pass

def print_warning(s):
    print(colored("PACUP WARNING: {}".format(s), "yellow"))

def print_normal(s=""):
    print(s)

def print_error(s):
    print(colored("PACUP ERROR: {}".format(s), "red"))

def print_success(s):
    print_green("PACUP: {}".format(s))

def print_additional_info(s):
    print(colored("PACUP INFO: {}".format(s), "cyan"))

def print_needed_info(s):
    print("PACUP: {}".format(s))

def print_needed_info_no_newline(s):
    print("PACUP: {}".format(s),end="")

def print_green(s):
    print(colored(s, "green"))

def print_cyan(s):
    print(colored(s, "cyan"))

def print_blue(s):
    print(colored(s, "cyan"))

def lazy_confirm(question):
    while True:
        print_needed_info_no_newline("{} [Y\\n]: ".format(question))
        ans = input()
        if ans == "n" or ans == "N":
            return False
        elif ans == "y" or ans == "Y" or ans == "":
            return True
        print_needed_info("Invalid input. Try again.\n")

def print_fill_width(char):
    w,_ = os.get_terminal_size()
    print_normal(w * char)
