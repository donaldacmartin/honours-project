from utilities.file.search import FileBrowser
from subprocess import call

PARALLEL   = ["parallel", "--no-notice"]
PYTHON     = ["python"]
BGP_PARSER = ["parallel/parse_bgp.py"]
BGP_MERGER = ["parallel/merge_bgp.py"]
SEPARATOR  = [":::"]

PARALLEL_PARSER = PARALLEL + PYTHON + BGP_PARSER + SEPARATOR
PARALLEL_MERGER = PARALLEL + PYTHON + BGP_MERGER + SEPARATOR

def get_list_of_files():
    root_dir   = "/nas05/users/csp/routing-data/archive.routeviews.org"
    files      = FileBrowser(root_dir)
    year_files = [files.get_year_end_files(year) for year in range(1997, 2014)]
    return [file for file in year_files if file is not None]

def organise_to_merge(year):
    merge_format = ""

    for bgp_file in year:
        merge_format += bgp_file + "|"

    return merge_format

all_files = get_list_of_files()

files_to_parse = [bgp_file for year in all_files for bgp_file in year]
files_to_merge = [organise_to_merge(year) for year in all_files]

print("Parsing files")
call(PARALLEL_PARSER + files_to_parse)

print("Merging parsed files")
call(PARALLEL_MERGER + files_to_merge)
