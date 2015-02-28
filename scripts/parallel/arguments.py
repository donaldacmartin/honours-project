from datetime import datetime

def get_country_code(arg):
    if len(arg) != 3:
        print("Country code must have 3 arguments")
        exit()

    return arg

def get_date(arg):
    try:
        day, month, year = arg.split("/")
        return datetime(int(year), int(month), int(day), 0)
    except:
        print("Date must be of form DD/MM/YYYY")
        exit()

def get_resolution(arg):
    try:
        width, height = arg.split("x")
        return int(width), int(height)
    except:
        print("Resolution must be of form WIDTHxHEIGHT")
        exit()
