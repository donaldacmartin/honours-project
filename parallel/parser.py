#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from utilities.parser.bgp import BGPParser
from utilities.parser.cisco import CiscoParser
from pickle import dump
from sys import argv

def dump_data(filename, parser_dump):
    output_filename = "temp/" + filename.replace("/", "_")
    output_file     = open(output_filename, "wb")

    dump(parser_dump, output_file)
    output_file.close()

if __name__ == "__main__":
    filename = argv[1]
    dump = BGPParser(filename) if "rib" in filename else CiscoParser(filename)
    dump_data(filename, dump)
