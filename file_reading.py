#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from subprocess import check_call, STDOUT
from tempfile import NamedTemporaryFile

PATH = "/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/"
CMD  = "bgpdump -m "
file_path = "2001.10/RIBS/rib.20011026.1648.bz2"

output = NamedTemporaryFile()
check_call([CMD, PATH + file_path], stdout=output, stderr=STDOUT)
output.seek(0)
print(f.read())