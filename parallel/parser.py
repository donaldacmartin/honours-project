#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from utilities.parser.bgp import BGPParser
from utilities.parser.cisco import CiscoParser
from pickle import dump
from sys import argv

def parse_dump(filename):
    parser = BGPParser(filename) if "rib" in filename else CiscoParser(filename)
    dump_data(filename, parser)

def dump_data(filename, parser):
    output_filename = "temp/" + filename.replace("/", "_")
    output_file     = open(output_filename, "wb")

    dump(parser, output_file)
    output_file.close()

if __name__ == "__main__":
    parse_dump(argv[1])
