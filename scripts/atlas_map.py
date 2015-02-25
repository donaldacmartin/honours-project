def get_router_files(date):
    root_dir = "/nas05/users/csp/routing-data/archive.routeviews.org"
    files    = FileBrowser(root_dir)
    return files.get_files_for_time(date.year, date.month, date.day, date.hour)

def get_index_file(files):
    parser_index = NamedTemporaryFile(mode="w", delete=False)

    for file in files:
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
            file   = open(filename, "r")
            parser = load(file, HIGHEST_PROTOCOL)

            file.close()
            parsers.append(parser)
        except:
            print("File",filename,"failed to load")

    return parsers

if __name__ == "__main__":
    region          = argv[1]
    date            = argv[2]
    resolution      = argv[2]
    output_filename = argv[4]

    print("Gathering a list of files to parse")
    bgp_files       = get_router_files(date)
    parallel_index  = get_index_file(bgp_files)
    print("Parsing BGP files in parallel")
    parsing_stdout  = run_parallel_parser(parallel_index)
    print("Collating parsed data")
    parsers         = read_in_parsers(parsing_stdout)
