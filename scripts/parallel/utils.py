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

def split_block_into_input_output(block):
    block_items = block.split("\n")
    block_items = [item for item in block_items if item.startswith("/")]

    if len(block_items) == 2:
        input_file  = block_items[0]
        output_file = block_items[1]
        return (input_file, output_file)

    raise Exception("Could read block: " + block)

def get_parser_dumps_from_parallel_stdout(parallel_stdout):
    stdout_blocks  = parallel_stdout.split("\n\n")
    dump_locations = {}

    for block in stdout_blocks:
        try:
            input_file, output_file    = split_block_into_input_output(block)
            dump_locations[input_file] = output_file
        except:
            continue

    return dump_locations

def create_merging_index_for_parallel(dump_locations, groups):
    merge_index_file = NamedTemporaryFile("w", delete=False)

    for group in groups:
        merge_index_line = ""

        for input_filename in group:
            if input_filename in dump_locations:
                merge_index_line += input_filename + "|"

        if merge_index_line == "":
            continue

        merge_index_line = merge_index_line[:-1] + "\n"
        merge_index_file.write(merge_index_line)

    merge_index_file.close()
    return merge_index_file.name

def merge_parsers(dump_locations, groups):
    merge_index_file = create_merging_index_for_parallel(dump_locations, groups)

    parallel_cmd = ["parallel", "--no-notice", "--group", "python",
                    "scripts/parallel/merge.py", "::::", merge_index_file]

    with NamedTemporaryFile() as f:
        check_call(parallel_cmd, stdout=f, stderr=STDOUT)
        f.seek(0)
        merged_parsers = f.read()

    merged_parsers = merged_parsers.split("\n")
    merged_parsers = [parser for parser in merged_parser if parser.startswith("/")]
    print(merged_parsers)
    merged_parsers = [load(open(parser, "r")) for parser in merged_parsers]
    return merged_parsers

"""
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
    filenames     = [filter_exceptions(block) for block in stdout_blocks]
    parsers       = {}

    for parsed_files in filenames:
        if parsed_files is None:
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
"""
