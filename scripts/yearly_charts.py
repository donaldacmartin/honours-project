from utilities.file.search import FileBrowser
from subprocess import check_output
from pickle import loads

from utilities.file.io import load_object
from visualisation.pyplot.pyplot_chart import YearlyChart
from visualisation.ring import RingGraph
from visualisation.chart.yearly_allocated_blocks import YearlyAllocatedBlocks
from visualisation.atlas.standard import StandardAtlas

PARALLEL   = ["parallel", "--no-notice", "--group", "--xapply"]
PYTHON     = ["python"]
BGP_PARSER = ["parallel/parse.py"]
SEPARATOR  = [":::"]

PARALLEL_PARSER = PARALLEL + PYTHON + BGP_PARSER + SEPARATOR
PARALLEL_MERGER = PARALLEL + PYTHON + BGP_MERGER + SEPARATOR

def get_list_of_files():
    root_dir   = "/nas05/users/csp/routing-data/archive.routeviews.org"
    files      = FileBrowser(root_dir)
    year_files = [files.get_year_end_files(year) for year in range(1997, 1999)]
    return [file for file in year_files if file is not None]

def run_gnu_parallel(command, arguments):
    return check_output(command + arguments)

def read_pickled_dumps_from_stdout(parsed_dumps):
    pickled_dumps = parsed_dumps.split("\r\n")
    lookup_map    = {}

    for pickled_dump in pickled_dumps:
        filename             = pickled_dump.split("\n")[0]
        dump_binary          = pickled_dump.split("\n")[1]
        lookup_map[filename] = dump_binary

    return lookup_map

def organise_dumps_for_merging(all_files, lookup_map):
    height = len(all_files)
    width  = max(len(year) for year in all_files)
    matrix = [[h for h in range(height)] + ":::" for w in range(width)]

    for column in range(width):
        for year in len(all_files):
            this_year = all_files[year]
            matrix[column][year] = lookup_map(this_year[column]) if column < len(this_year) else "-"

    matrix[-1].pop()
    return matrix

def read_dumps_and_sort():
    pass

def draw_chart(files):
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

if __name__ == "__main__":
    all_files      = get_list_of_files()
    files_to_parse = [bgp_file for year in all_files for bgp_file in year]
    parsed_dumps   = run_gnu_parallel(PARALLEL_PARSER, files_to_parse)
    pickled_dumps  = read_pickled_dumps_from_stdout(parsed_dumps)
    dumps_to_merge = organise_dumps_for_merging(pickled_dumps)
    merged_dumps   = run_gnu_parallel(PARALLEL_MERGER, dumps_to_merge)
