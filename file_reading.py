#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from subprocess import check_output, STDOUT
from tempfile import NamedTemporaryFile

PATH = "/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/"
CMD  = "bgpdump -m <filename>"

output = NamedTemporaryFile()
check_call([CMD, PATH + file_path], stdout=output, stderr=STDOUT)
output.seek(0)
print(f.read())