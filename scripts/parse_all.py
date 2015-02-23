from utilities.file.search import FileBrowser
from tempfile import NamedTemporaryFile
from subprocess import Popen, PIPE

parallel_cmd = ["parallel", "--no-notice", "--group", "-a", "file" "python",
                "parallel/parse.py",]

root_dir     = "/nas05/users/csp/routing-data/archive.routeviews.org"
files        = FileBrowser(root_dir)
years        = [files.get_year_end_files(year) for year in range(1997, 2014)]

parser_index = NamedTemporaryFile(mode="w", delete=True)

for year in years:
    for file in years:
        parser_index.write(file[0] + "\n")

parser_index.close()

parser_cmd[4]  = parser_index.name
parallel_parse = Popen(parallel_cmd, stdout=PIPE, stderr=PIPE)
stdout, stderr = parallel_parse.communicate()
