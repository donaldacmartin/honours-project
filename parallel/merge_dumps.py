from utilities.parser.merged import MergedParser
from pickle import load

def merge_dumps(files):
    files   = files.split("|")
    parsers = []

    for f in files:
        parsers.append(unpickle_dump("temp/" + f.replace("/", "_")))

    if len(files) < 2:
        dump_data(files[0], parsers[0])
        return

    final_parser = MergedParser(parsers.pop(), parsers.pop())

    while len(parsers) > 0:
        final_parser = MergedParser(final_parser, parsers.pop())

    dump_data(files[0], final_parser)

def unpickle_dump(filename):
    pickle_file = open(filename, "rb")
    bgp_file = load(pickle_file)

    pickle_file.close()
    return bgp_file

def dump_data(filename, parser):
    output_filename = "temp/merged" + filename.replace("/", "_")
    output_file     = open(output_filename, "wb")

    dump(parser, output_file)
    output_file.close()
