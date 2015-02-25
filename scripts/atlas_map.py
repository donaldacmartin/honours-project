from sys import argv
from datetime import datetime
from utilities.file.search import FileBrowser
from tempfile import NamedTemporaryFile
from subprocess import check_output
from pickle import load
from parser.merged import MergedParser
from visualisation.atlas.standard import StandardAtlas

def get_router_files(date):
    root_dir = "/nas05/users/csp/routing-data/archive.routeviews.org"
    files    = FileBrowser(root_dir)
    return files.get_files_for_time(date.year, date.month, date.day, 00)

def get_index_file(files):
    parser_index = NamedTemporaryFile(mode="w", delete=False)

    for file in files:
        parser_index.write(file + "\n")

    parser_index.close()
    return parser_index.name

def run_parallel_parser(index_file_name):
    parallel_cmd   = ["parallel", "--no-notice", "--group", "python",
                      "parallel/parse.py", "::::", index_file_name]

    return check_output(parallel_cmd)

def read_in_parsers(parallel_stdout):
    filenames = parallel_stdout.split("\n")
    parsers   = []

    for filename in filenames:
        try:
            file   = open(filename, "r")
            parser = load(file)

            file.close()
            parsers.append(parser)
        except:
            print("File",filename,"failed to load")

    return parsers

def merge_parsers(parsers):
    if len(parsers) == 1:
        return parsers[0]

    merged_parser = MergedParser(parsers[0], parsers[1])

    for i in range(2, len(parsers)):
        merged_parser = MergedParser(parsers[i], merged_parser)

    return merged_parser

def generate_graph(parser, width, height, region):
    return StandardAtlas(parser, width, height)

if __name__ == "__main__":
    region          = argv[1]
    date            = argv[2]
    resolution      = argv[3]
    output_filename = argv[4]

    try:
        width, height = resolution.split("x")
    except:
        print("Resolution should be WIDTHxHEIGHT in pixels")
        exit()

    try:
        day, month, year = date.split("/")
        date = datetime(int(year), int(month), int(day))
    except:
        print("Date should be format DD/MM/YYYY")
        exit()

    print("Gathering a list of files to parse")
    bgp_files = get_router_files(date)
    parallel_index = get_index_file(bgp_files)

    print("Parsing BGP files in parallel (" + str(len(bgp_files)) + ")")
    parsing_stdout = run_parallel_parser(parallel_index)

    print("Collating parsed data")
    parsers = read_in_parsers(parsing_stdout)
    parser = merge_parsers(parsers)
    graph = generate_graph(parser, int(width), int(height), region)
    graph.save(output_filename)
