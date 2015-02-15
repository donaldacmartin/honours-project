#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from utilities.parser.mrt import MRTParser
from utilities.parser.cisco import CiscoParser
from pickle import dumps, HIGHEST_PROTOCOL
from sys import argv

"""
Parse

Allows GNU Parallel to run parsers in parallel and dumps the contents to STDOUT.
"""

def parse_file(filename):
    parser = MRTParser(filename) if "rib" in filename else CiscoParser(filename)
    binary = dumps(parser, HIGHEST_PROTOCOL)
    print("\r\n" + filename + "\n" + binary)

if __name__ == "__main__":
    parse_file(argv[1])
