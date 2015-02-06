from utilities.file.search import FileBrowser
from subprocess import call
from os.path import exists
from os import makedirs

from utilities.file.io import load_object
from graphs.pyplot.pyplot_chart import YearlyChart
from graphs.ring import RingGraph
from graphs.chart.yearly_allocated_blocks import YearlyAllocatedBlocks
from graphs.atlas.standard import StandardAtlas

PARALLEL   = ["parallel", "--no-notice"]
PYTHON     = ["python"]
BGP_PARSER = ["parallel/parse_bgp.py"]
BGP_MERGER = ["parallel/merge_bgp.py"]
SEPARATOR  = [":::"]

PARALLEL_PARSER = PARALLEL + PYTHON + BGP_PARSER + SEPARATOR
PARALLEL_MERGER = PARALLEL + PYTHON + BGP_MERGER + SEPARATOR

def create_directory(directory):
    if not exists(directory):
        makedirs(directory)

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

def draw_chart(files):
    dumps = [load_object("temp/merged", file) for file in files]

    generic_chart = YearlyChart(dumps)
    generic_chart.draw_address_space("address-space.png")
    generic_chart.draw_most_common_block_size("most-common-block-size.png")
    generic_chart.draw_stacked_allocation_of_blocks("stacked-allocation.png")

    y = YearlyAllocatedBlocks(dumps)
    y.save("yearly-blocks.png")

    s = StandardAtlas(dumps[-1])
    s.save("standard-atlas.png")

    r = RingGraph(dumps[-1])
    r.save("ring-graph.png")

all_files = get_list_of_files()
files_to_parse = [bgp_file for year in all_files for bgp_file in year]
files_to_merge = [organise_to_merge(year) for year in all_files]
files_to_chart = [files[0] for files in files_to_merge]

print("Parsing files")
create_directory("temp/parsed")
call(PARALLEL_PARSER + files_to_parse)

print("Merging parsed files")
create_directory("temp/merged")
call(PARALLEL_MERGER + files_to_merge)

print("Drawing chart")
draw_chart(files_to_chart)
