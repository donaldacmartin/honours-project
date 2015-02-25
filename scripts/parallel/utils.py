from utilities.file.search import FileBrowser
from subprocess import check_output
from tempfile import NamedTemporaryFile
from pickle import load
from parser.merged import MergedParser

def get_router_files(yy, mm, dd):
    root_dir = "/nas05/users/csp/routing-data/archive.routeviews.org"
    files    = FileBrowser(root_dir)
    return files.get_files_for_time(yy, mm, dd, 00)

def run_parallel_parser(index_file_name):
    parallel_cmd   = ["parallel", "--no-notice", "--group", "python",
                      "scripts/parallel/parse.py", "::::", index_file_name]

    return check_output(parallel_cmd)

def get_index_file(files):
    parser_index = NamedTemporaryFile(mode="w", delete=False)

    for file in files:
        parser_index.write(file + "\n")

    parser_index.close()
    return parser_index.name

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
