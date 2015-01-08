from utilities.parser.bgp import BGPParser
from utilities.parser.cisco import CiscoParser
from pickle import dump
from sys import argv

def parse_file(filename):
    parser = BGPParser(filename) if "rib" in filename else CiscoParser(filename)
    pickle_parser(parser)

def pickle_parser(filename, parser):
    output_file = open("temp/parsed/" + filename.replace("/", "_"))
    dump(parser, output_file)
    output_file.close()

if __name__ == "__main__":
    parse_file(argv[1])
