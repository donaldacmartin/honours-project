from scripts.plot_chart import *
from time import time

if __name__ == "__main__":
    start = time()
    address_space, yearly_blocks, most_common_alloc, stacked_alloc, width, height = organise_arguments()
    end = time()
    print("Time to parse arguments: " + str(end - start) + " seconds")

    start = time()
    bgp_files      = get_router_files_for_years(1997, 2014)
    parallel_index = get_index_file_2d_list(bgp_files)
    end = time()
    print("Time to choose files: " + str(end - start) + " seconds")

    print("Parsing BGP files in parallel (" + str(len(bgp_files)) + ")")
    start = time()
    parsing_stdout = run_parallel_parser(parallel_index)
    end = time()
    print("Time to parse files: " + str(end - start) + " seconds")

    start = time()
    parsers          = read_in_parsers(parsing_stdout)
    parsers_by_year  = sort_parsers_into_years(parsers)
    parser_for_years = merge_yearly_parsers(parsers_by_year)
    end = time()
    print("Time to collate files: " + str(end - start) + " seconds")

    start = time()
    chart = YearlyChart(parser_for_years, width, height)

    if address_space:
        chart.draw_address_space("address-space.png")

    if most_common_alloc:
        chart.draw_most_common_block_size("most-common-block-size.png")

    if stacked_alloc:
        chart.draw_stacked_allocation_of_blocks("stacked-allocation.png")

    if yearly_blocks:
        YearlyAllocatedBlocks(parser_for_years).save("yearly-blocks.png")

    end = time()
    print("Time to draw chart: " + str(end - start) + " seconds")
