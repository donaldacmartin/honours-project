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

def merge_dumps(pickled_dumps):
    base_dump = loads(pickled_dumps.pop())

    while len(files) > 1:
        next_dump = pickled_dumps.pop()

        if next_dump == "-":
            continue

        next_dump = loads(pickled_dumps.pop())
        base_dump = MergedParser(base_dump, next_dump)

    return dumps(base_dump)

if __name__ == "__main__":
    argv.pop()
    merged_dump = merge_dumps(argv)
    print("\r\n" + merged_dump)
