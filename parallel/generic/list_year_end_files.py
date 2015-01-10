#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from utilities.file.search import FileBrowser

"""
Writes a list of year-end filenames for parallel parsing and merging.
"""

def create_list_of_files():
    root_dir = "/nas05/users/csp/routing-data/archive.routeviews.org"
    database = FileBrowser(root_dir)
    years    = []

    for year in range(1997, 2014):
        years.append(database.get_year_end_files(year))

    years = [year for year in years if year is not None]
    write_index_for_parallel_parsing(years)
    write_index_for_merging(years)

def write_index_for_parallel_parsing(years):
    file = open("temp/files_to_parse", "wb")

    for year in years:
        for router in year:
            file.write(router + "\n")

    file.close()

def write_index_for_merging(years):
    file = open("temp/files_to_merge", "wb")

    for year in years:
        for router in year:
            file.write(router + "|")
        file.write("\n")

    file.close()

if __name__ == "__main__":
    create_list_of_files()
