#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from utilities.bgp import BGPDumpExecutor
from pickle import dump
from sys import argv

def parse_bgp(filename):
    bgp = BGPDumpExecutor(filename)

    output_filename = "temp" + filename
    output_file     = open(output_filename, "wb")

    dump(bgp, output_file)

if __name__ == "__main__":
    parse_bgp(argv[1])
