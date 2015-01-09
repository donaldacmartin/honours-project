#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from utilities.parser.mrt import MRTParser
from utilities.parser.cisco import CiscoParser
from utilities.file.io import save_object
from sys import argv

"""
Parse

Allows GNU Parallel to run parsers in parallel and dumps the contents into a
temporary directory.
"""

def parse_file(filename):
    parser = BGPParser(filename) if "rib" in filename else CiscoParser(filename)
    save_object("temp/parsed", filename, parser)

if __name__ == "__main__":
    parse_file(argv[1])
