#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from parser.exception import *
from parser.mrt import MRTParser
from parser.cisco import CiscoParser
from pickle import dump, HIGHEST_PROTOCOL
from tempfile import NamedTemporaryFile
from sys import argv

def parse_file(filename):
    return MRTParser(filename) if "rib" in filename else CiscoParser(filename)

def dump_to_file_and_get_filename(parser):
    file = NamedTemporaryFile("w", delete=False)
    dump(parser, file, HIGHEST_PROTOCOL)
    file.close()
    return file.name

if __name__ == "__main__":
    input_file  = argv[1]

    try:
        parser = parse_file(input_file)
        output_filename = dump_to_file_and_get_filename(parser)
        print(output_filename)
        with open("log.out", "a") as log:
            log.write("I'm done\n")
    except ParserError as e:
        print("Fatal parser error encountered " + str(e))
    except IOError as e:
        print("Fatal I/O error encountered " + str(e))
