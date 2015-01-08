from utilities.parser.merged import MergedParser
from pickle import load, dump
from sys import argv

def merge_dumps(files):
    files = files.split("|")
    name  = files[0]

    if len(files) < 2:
        parser = open_dump(files[0])
        save_dump(parser)

    final_parser = MergedParser(files.pop(), files.pop())

    while len(files) > 1:
        final_parser = MergedParser(final_parser, files.pop())

    save_dump(name, parser)

def open_dump(filename):
    pickle_file = open("temp/parsed/" + filename.replace("/", "_"), "rb")
    parser      = load(pickle_file)
    pickle_file.close()
    return parser

def save_dump(filename, parser):
    output_file = open("temp/merged/" + filename.replace("/", "_"), "wb")
    dump(parser, output_file)
    output_file.close()

if __name__ == "__main__":
    merge_dumps(argv[1])
