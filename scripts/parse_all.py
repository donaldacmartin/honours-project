from utilities.file.search import FileBrowser
from tempfile import NamedTemporaryFile
from subprocess import check_output
from pickle import load, HIGHEST_PROTOCOL
from visualisation.pyplot.pyplot_chart import YearlyChart
from sys import argv

def get_yearly_files(start_year, end_year):
    root_dir = "/nas05/users/csp/routing-data/archive.routeviews.org"
    files    = FileBrowser(root_dir)
    return [files.get_year_end_files(year) for year in range(start_year, end_year)]

def get_index_file(yearly_files):
    parser_index = NamedTemporaryFile(mode="w", delete=False)

    for year in yearly_files:
        for file in year:
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
            parser = load(filename, HIGHEST_PROTOCOL)
            parsers.append(parser)
        except:
            print("File",filename,"failed to load")

    return parsers

def draw_charts(parsers):
    chart = YearlyChart(dumps)
    chart.draw_address_space("address-space.png")
    chart.draw_most_common_block_size("most-common-block-size.png")
    chart.draw_stacked_allocation_of_blocks("stacked-allocation.png")

if __name__ == "__main__":
    start_year     = int(argv[1])
    end_year       = int(argv[2])

    yearly_files   = get_yearly_files(start_year, end_year)
    index_file     = get_index_file(yearly_files)
    parse_result   = run_parallel_parser(index_file)
    parsers        = read_in_parsers(parse_result)
    sorted_parsers = sorted(parsers, key=lambda p: p.datetime, reverse=True)
    draw_charts(sorted_parsers)
