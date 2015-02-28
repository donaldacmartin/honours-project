
def organise_args():
    if len(argv) != 6:
        print("Incorrect argument usage")
        print("Arguments: COUNTRY_ISO3 START_DATE END_DATE OUTPUT_FILENAME")
        exit()

    country_iso     = get_country_code(argv[1])
    start_date      = get_date(argv[2])
    end_date        = get_date(argv[3])
    width, height   = get_resolution(argv[4])
    output_filename = argv[5]

    return country_code, start_date, end_date, resolution, output_filename

def get_country_code(arg):
    if len(arg) != 3:
        print("Country code must have 3 arguments")
        exit()

    return arg

def get_date(arg):
    try:
        day, month, year = arg.split("/")
        return int(day), int(month), int(year)
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

n = NationalDownTimeChart(parsers, "EGY", "egypt-down.png")

if __name__ == "__main__":
    country, start, end, resolution, output = organise_args()
    
