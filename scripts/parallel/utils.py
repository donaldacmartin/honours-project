from utilities.file.search import FileBrowser
from commands import getoutput
from subprocess import check_call, STDOUT
from tempfile import NamedTemporaryFile
from pickle import load
from parser.merged import MergedParser

def get_router_files_for_date(yy, mm, dd, hh=0):
    root_dir = "/nas05/users/csp/routing-data/archive.routeviews.org"
    files    = FileBrowser(root_dir)
    return files.get_files_for_time(yy, mm, dd, hh)

def get_router_files_for_years(start, end):
    root_dir   = "/nas05/users/csp/routing-data/archive.routeviews.org"
    files      = FileBrowser(root_dir)
    year_files = [files.get_year_end_files(year) for year in range(start, end)]
    return [file for file in year_files if file is not None]

def run_parallel_parser(index_file_name):
    parallel_cmd = ["parallel", "--no-notice", "--group", "python",
                    "scripts/parallel/parse.py", "::::", index_file_name]

    with NamedTemporaryFile() as f:
        check_call(parallel_cmd, stdout=f, stderr=STDOUT)
        f.seek(0)
        output = f.read()

    return output

def get_index_file(files):
    parser_index = NamedTemporaryFile(mode="w", delete=False)

    for file in files:
        parser_index.write(file + "\n")

    parser_index.close()
    return parser_index.name

def get_index_file_2d_list(years):
    parser_index = NamedTemporaryFile(mode="w", delete=False)

    for year in years:
        for file in year:
            parser_index.write(file + "\n")

    parser_index.close()
    return parser_index.name

def filter_exceptions(stdout_block):
    blocks = stdout_block.split("\n")
    blocks = [block for block in blocks if block.startswith("/")]

    if "error" in blocks:
        return None

    return blocks if len(blocks) == 2 else None

def read_in_parser(input_filename, output_filename, list_of_parsers):
    try:
        file   = open(output_filename, "r")
        parser = load(file)

        file.close()
        list_of_parsers[input_filename] = parser
    except:
        print("File",output_filename,"failed to load")

    return list_of_parsers

def read_in_parsers(parallel_stdout):
    stdout_blocks = parallel_stdout.split("\n\n")
    filenames     = [filter_exceptions(file) for file in filename]
    parsers       = {}

    for parsed_files in filenames:
        if parsed_file is None:
            continue

        input_filename  = parsed_files[0]
        output_filename = parsed_files[1]

        parsers = read_in_parser(input_filename, output_filename, parsers)
    return parsers

def merge_parsers(parsers, groups=None):
    file = NamedTemporaryFile("w", delete=False)

    if groups is None:
        file.write("|".join(parsers.values()))
    else:
        for group in groups:
            files_to_merge = [parsers[f] for f in group]
            line_format    = "|".join(files_to_merge)
            file.write(line_format + "\n")

    file.close()
    parallel_cmd = ["parallel", "--no-notice", "--group", "python",
                    "scripts/parallel/merge.py", "::::", file.name]

    with NamedTemporaryFile() as f:
        check_call(parallel_cmd, stdout=f, stderr=STDOUT)
        f.seek(0)
        merged_parsers = f.read()

    completed_parsers = []

    for parser in merged_parsers:
        completed_parsers = load(parser)

    return completed_parsers if len(completed_parsers) > 1 else completed_parsers[0]
