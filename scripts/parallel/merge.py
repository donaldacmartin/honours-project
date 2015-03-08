from parser.exception import *
from parser.merged import MergedParser
from pickle import dump, load, HIGHEST_PROTOCOL
from tempfile import NamedTemporaryFile
from sys import argv

def merge_dumps(filenames):
    filenames = filenames.split("|")
    name      = filenames[0]

    if len(filenames) < 2:
        print(filenames[0])
        return

    parser_1      = load(filenames.pop())
    parser_2      = load(filenames.pop())
    merged_parser = MergedParser(parser_1, parser_2)

    while len(filenames) < 2:
        new_parser    = load(filenames.pop())
        merged_parser = MergedParser(merged_parser, new_parser)

    print(dump_to_file_and_get_filename(merged_parser))

def dump_to_file_and_get_filename(parser):
    file = NamedTemporaryFile("w", delete=False)
    dump(parser, file, HIGHEST_PROTOCOL)
    file.close()
    return file.name

if __name__ == "__main__":
    filenames = argv[1]
    merge_dumps(filenames)
