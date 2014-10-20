#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from subprocess import check_call, STDOUT
from tempfile import NamedTemporaryFile

PATH = "/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/"
CMD  = "bgpdump -m " + PATH
file_path = CMD + "2001.10/RIBS/rib.20011026.1648.bz2"
"""
print("File : " + PATH + file_path)
output = NamedTemporaryFile()
check_call([file_path], stdout=output, stderr=STDOUT)
output.seek(0)
print(output.read())
"""
with NamedTemporaryFile() as f:
    check_call([file_path], stdout=f, stderr=STDOUT)
    f.seek(0)
    print(f.read())