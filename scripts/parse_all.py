from utilities.file.search import FileBrowser
from tempfile import NamedTemporaryFile
from subprocess import call

parallel_cmd = ["parallel", "--no-notice", "--group" "python",
                "parallel/parse.py", "::::"]

root_dir     = "/nas05/users/csp/routing-data/archive.routeviews.org"
files        = FileBrowser(root_dir)
years        = [files.get_year_end_files(year) for year in range(1997, 2014)]

parser_index = NamedTemporaryFile(mode="w", delete=False)

for year in years:
    for file in years:
        parser_index.write(file[0] + "\n")

parser_index.close()

parallel_cmd    += [parser_index.name]
parallel_parse  =  call(parallel_cmd)
print(parallel_parse)
