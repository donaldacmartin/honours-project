#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from utilities.parser.mrt import MRTParser
from utilities.parser.cisco import CiscoParser
from pickle import dump, HIGHEST_PROTOCOL
from sys import argv

"""
Parse


"""

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
        parser      = parse_file(input_file)
        output_file = dump_to_file_and_get_filename(output_file, parser)
        print(input_file + "\n" + output_file + "\n\n")
    except ParserError as e:
        print("Fatal parser error encountered " + str(e))
    except IOError as e:
        print("Fatal I/O error encountered " + str(e))
