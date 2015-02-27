from sys import argv
from parallel.utils import *

from visualisation.atlas.standard import StandardAtlas
#from visualisation.atlas.heat import HeatAtlas
from visualisation.ring.standard import StandardRing
from visualisation.ring.staggered import StaggeredRing

def organise_arguments():
    if not 5 <= len(argv) <= 6:
        print("Incorrect argument usage")
        print("Arguments: GRAPH_TYPE DATE RESOLUTION [REGION] OUTPUT_FILENAME")
        exit()

    graph_type       = get_graph_type(argv[1])
    year, month, day = get_date_from_args(argv[2])
    width, height    = get_resolution_from_args(argv[3])
    region           = None if len(argv) < 6 else argv[4]
    output_filename  = argv[4] if len(argv) < 6 else argv[5]

    return graph_type, year, month, day, width, height, region, output_filename

def get_date_from_args(arg):
    try:
        day, month, year = arg.split("/")
        return int(year), int(month), int(day)
    except:
        print("Date should be format DD/MM/YYYY")
        exit()

def get_resolution_from_args(arg):
    try:
        width, height  = arg.split("x")
        return int(width), int(height)
    except:
        print("Resolution should be WIDTHxHEIGHT in pixels")
        exit()

def get_graph_type(arg):
    graph_types = ["STANDARD_ATLAS", "HEAT_ATLAS", "STANDARD_RING",
                   "STAGGERED_RING"]

    if arg not in graph_types:
        print("Invalid graph type")
        print("Options are: ")

        for graph in graph_types:
            print("- " + graph)

        exit()

    return arg

def generate_graph(graph_type, parser, width, height, region):
    if graph_type == "STANDARD_ATLAS":
        return StandardAtlas(parser, width, height)
    #elif graph_type == "HEAT_ATLAS":
    #    return HeatAtlas(parser, width, height)
    elif graph_type == "STANDARD_RING":
        return StandardRing(parser, width, height)
    elif graph_type == "STAGGERED_RING":
        return StaggeredRing(parser, width, height)

if __name__ == "__main__":
    year, month, day, width, height, region, graph_type, output_filename = organise_arguments()

    print("Gathering a list of files to parse")
    bgp_files = get_router_files(year, month, day)
    parallel_index = get_index_file(bgp_files)

    print("Parsing BGP files in parallel (" + str(len(bgp_files)) + ")")
    parsing_stdout = run_parallel_parser(parallel_index)

    print("Collating parsed data")
    parsers = read_in_parsers(parsing_stdout)
    parser  = merge_parsers(parsers)

    print("Drawing graph")
    graph = generate_graph(parser, width, height, region)
    graph.save(output_filename)
