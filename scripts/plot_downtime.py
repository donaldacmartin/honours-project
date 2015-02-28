from datetime import datetime, timedelta
from parallel.utils import *
from parallel.arguments import *
from visualisation.pyplot.national_downtime import NationalDownTimeChart

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

    return country_code, start_date, end_date, width, height, output_filename

def get_files_to_parse(start_date, end_date):
    date           = start_date
    delta          = timedelta(hours=2)
    files_to_parse = []

    while date < end_date:
        files = get_router_files_for_date(date.year, date.month, date.day, date.hour)
        files_to_parse.append(files)
        date += delta

    total_files = sum([len(date_files) for date_files in files_to_parse])
    return files_to_parse, total_files

def organise_for_merging(unsorted_parsers):
    sorted_parsers    = {}
    ready_for_merging = []

    for parser in unsorted_parsers:
        parser_datetime = parser.datetime

        if parser_datetime in sorted_parsers:
            sorted_parsers[parser_datetime].append(parser)
        else:
            sorted_parsers[parser_datetime] = [parser]

    for date in sorted(sorted_parsers):
        parsers = sorted_parsers[date]
        ready_for_merging.append(parsers)

    return ready_for_merging

def merge_grouped_parsers(unmerged_parser_groups):
    merged_parsers = []

    for group in unmerged_parser_groups:
        merged_parser = merge_parsers(group)
        merged_parsers.append(merged_parser)

    return merged_parsers

n = NationalDownTimeChart(parsers, "EGY", "egypt-down.png")

if __name__ == "__main__":
    country, start, end, width, height, output = organise_args()

    print("Getting files to parse")
    files_to_parse, number_of_files = get_files_to_parse(start, end)
    index_file                      = get_index_file_2d_list(files_to_parse)

    print("Parsing in parallel " + str(number_of_files) + " files")
    parallel_stdout  = run_parallel_parser(index_file)
    unsorted_parsers = read_in_parsers(parallel_stdout)

    print("Merging parsed data")
    grouped_parsers  = organise_for_merging(unsorted_parsers)
    merged_parsers   = merge_grouped_parsers(grouped_parsers)

    print("Plotting graph")
    NationalDownTimeChart(merged_parsers, country, output)
