from termcolor import colored

class PacupUserError(Exception):
    pass

class PacupUnknownError(Exception):
    pass

def print_warning(s):
    print(colored("PACUP WARNING: {}".format(s), "yellow"))

def print_normal(s):
    print(s)

def print_error(s):
    print(colored("PACUP ERROR: {}".format(s), "red"))

def print_success(s):
    print_green("PACUP: {}".format(s))

def print_additional_info(s):
    print(colored("PACUP INFO: {}".format(s), "green"))

def print_needed_info(s):
    print("PACUP: {}".format(s))

def print_green(s):
    print(colored(s, "green"))

def print_cyan(s):
    print(colored(s, "cyan"))

def print_blue(s):
    print(colored(s, "blue"))
