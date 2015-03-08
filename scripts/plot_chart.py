from sys import argv
from parallel.utils import *
from parallel.arguments import *
from visualisation.pyplot.chart import YearlyChart
from visualisation.chart.yearly_allocated_blocks import YearlyAllocatedBlocks

def organise_arguments():
    address_space     = True if "ADDRESS_SPACE" in argv else False
    yearly_blocks     = True if "YEARLY_BLOCKS" in argv else False
    most_common_alloc = True if "MOST_COMMON_ALLOC" in argv else False
    stacked_alloc     = True if "STACKED_ALLOC" in argv else False
    width, height     = get_resolution(argv[-1])

    return address_space, yearly_blocks, most_common_alloc, stacked_alloc, width, height

def sort_parsers_into_years(parsers):
    years = {}

    for parser in parsers:
        year = parser.datetime.year

        if year in years:
            years[year].append(parser)
        else:
            years[year] = [parser]

    return years

if __name__ == "__main__":
    address_space, yearly_blocks, most_common_alloc, stacked_alloc, width, height = organise_arguments()

    print("Gathering a list of files to parse")
    bgp_files      = get_router_files_for_years(1997, 2000)
    parallel_index = get_index_file_2d_list(bgp_files)

    print("Parsing BGP files in parallel (" + str(len(bgp_files)) + ")")
    parsing_stdout = run_parallel_parser(parallel_index)

    print("Collating parsed data")
    parsers         = read_in_parsers(parsing_stdout)
    merged_parsers  = merge_parsers(parsers, bgp_files)
    parsers_by_year = sort_parsers_into_years(merged_parsers)

    print("Drawing charts")
    chart = YearlyChart(parsers_by_year, width, height)

    if address_space:
        chart.draw_address_space("address-space.png")

    if most_common_alloc:
        chart.draw_most_common_block_size("most-common-block-size.png")

    if stacked_alloc:
        chart.draw_stacked_allocation_of_blocks("stacked-allocation.png")

    if yearly_blocks:
        YearlyAllocatedBlocks(parser_for_years).save("yearly-blocks.png")
