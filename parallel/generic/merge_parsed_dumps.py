#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from utilities.parser.merged import MergedParser
from utilities.file.io import load_object, save_object
from sys import argv

"""
Merge

Allows GNU Parallel to merge the data collected from several routers into one
BGP dataset for interpretation.
"""

def merge_dumps(files):
    files = [f for f in files.split("|") if f != ""]
    name  = files[0]

    if len(files) < 2:
        parser = load_object("temp/parsed", files[0])
        save_object(name, parser)
        return

    parser1 = load_object("temp/parsed", files.pop())
    parser2 = load_object("temp/parsed", files.pop())
    final_parser = MergedParser(parser1, parser2)

    while len(files) > 1:
        parser = load_object("temp/parsed", files.pop())
        final_parser = MergedParser(final_parser, parser)

    save_object("temp/merged", name, parser)

if __name__ == "__main__":
    merge_dumps(argv[1])
