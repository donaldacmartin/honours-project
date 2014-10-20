#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from subprocess import Popen
from shlex import split
from tempfile import NamedTemporaryFile

COMMAND = "bgpdump -m "
PATH = "/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/"
commands = "bgpdump -m /nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/2001.10/RIBS/rib.20011026.1648.bz2"

def read_binary_into_ascii(filename):
    temp_file = NamedTemporaryFile()
    cmd = COMMAND + PATH + filename
    args = split(cmd)
    p = Popen(args, stdout=temp_file)
    temp_file.seek(0)
    return temp_file
    
t = read_binary_into_ascii("2001.10/RIBS/rib.20011026.1648.bz2")

while True:
    input()
    t.seek(0)
    print(t.readline())