from utilities.file.search import FileBrowser
from tempfile import NamedTemporaryFile
from subprocess import call
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
    return call(parallel_cmd)

if __name__ == "__main__":
    start_year      = int(argv[1])
    end_year        = int(argv[2])
    # output_filename = argv[3]

    yearly_files    = get_yearly_files(start_year, end_year)
    index_file      = get_index_file(yearly_files)
    print(index_file)
    parse_result    = run_parallel_parser(index_file)
