#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from utilities.file_search import FileBrowser
from os import mkdir

def list_files():
    files = FileBrowser("/nas05/users/csp/routing-data/archive.routeviews.org")
    dumps = []

    for year in range(1997, 2014):
        dumps += files.get_year_end_files(year)

def output(files):
    mkdir("temp")
    output_file = open("temp/dumps", "w+")

    for dump in files:
        output_file.write(dump + "\n")

    output_file.close()

if __name__ == "__main__":
    list_files()
