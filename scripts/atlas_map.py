from sys import argv
from parallel.utils import *
from visualisation.atlas.standard import StandardAtlas

def organise_arguments():
    if len(argv) != 5:
        print("Incorrect argument usage")
        print("Use python atlas_map.py REGION DATE RESOLUTION OUTPUT_FILENAME")
        exit()

    args = {}
    args = get_date_from_args(args)
    args = get_resolution_from_args(args)

    args["region"] = argv[1]
    args["output"] = argv[4]

    return args

def get_date_from_args(args):
    try:
        day, month, year = argv[2].split("/")
        args["day"]      = int(day)
        args["month"]    = int(month)
        args["year"]     = int(year)
        return args
    except:
        print("Date should be format DD/MM/YYYY")
        exit()

def get_resolution_from_args(args):
    try:
        width, height  = argv[3].split("x")
        args["width"]  = int(width)
        args["height"] = int(height)
        return args
    except:
        print("Resolution should be WIDTHxHEIGHT in pixels")
        exit()

def generate_graph(parser, width, height, region):
    return StandardAtlas(parser, width, height)

if __name__ == "__main__":
    args = organise_arguments()

    print("Gathering a list of files to parse")
    bgp_files = get_router_files(args["year"], args["month"], args["date"])
    parallel_index = get_index_file(bgp_files)

    print("Parsing BGP files in parallel (" + str(len(bgp_files)) + ")")
    parsing_stdout = run_parallel_parser(parallel_index)

    print("Collating parsed data")
    parsers = read_in_parsers(parsing_stdout)
    parser = merge_parsers(parsers)
    graph = generate_graph(parser, args["width"], args["height"], args["region"])
    graph.save(args["output"])
