from utilities.parser.merged import MergedParser
from pickle import load, dump
from sys import argv

def merge_dumps(files):
    files = [f for f in files.split("|") if f != ""]
    name  = files[0]

    if len(files) < 2:
        parser = open_dump(files[0])
        save_dump(name, parser)

    parser1 = open_dump(files.pop())
    parser2 = open_dump(files.pop())
    final_parser = MergedParser(parser1, parser2)

    while len(files) > 1:
        parser = open_dump(files.pop())
        final_parser = MergedParser(final_parser, parser)

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
