#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from utilities.file_search import FileBrowser
from os import mkdir

def list_files():
    files = FileBrowser("/nas05/users/csp/routing-data/archive.routeviews.org")

    all_files    = []
    yearly_files = []

    for year in range(1997, 2014):
        this_year = files.get_year_end_files(year)
        all_files += this_year
        yearly_files.append(this_year)

    output_all(all_files)
    output_years(yearly_files)
    output_merged_names(yearly_files)

def output_all(files):
    output_file = open("temp/dumps", "w+")

    for filename in files:
        output_file.write(filename + "\n")

    output_file.close()

def output_years(yearly_files):
    years_file  = open("temp/years", "w+")
    merged_file = open("temp/merged", "w+")

    for year in yearly_files:
        merged_file.write(year[0] + "\n")

        for filename in year:
            years_file.write(filename + "|")

        years_file.write("\n")

    years_file.close()
    merged_file.close()

if __name__ == "__main__":
    list_files()
