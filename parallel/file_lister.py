#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from utilities.file_search import get_bgp_binaries_in
from os.path import exists
from os import mkdir

def list_files():
    base_dir = "/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/"
    bgp_files = get_bgp_binaries_in(base_dir)
    sorted_files = sort_files(bgp_files)
    write_to_file("bgp_files", sorted_files)

    list1 = sorted_files[:-1]
    list2 = sorted_files[1:]

    write_to_file("graph_args_1", list1)
    write_to_file("graph_args_2", list2)

def sort_files(bgp_files):
    sorted_files = []

    for year in range(2001, 2015):
        for month in range(1, 13):
            name_identifier = "rib." + str(year) + str(month).zfill(2) + "01"

            for bgp_file in bgp_files:
                if name_identifier in bgp_file:
                    sorted_files.append(bgp_file)
                    break

    return sorted_files

def write_to_file(filename, sorted_files):
    if not exists("temp"):
        mkdir("temp")

    output_file = open("temp/" + filename, "w+")

    for bgp_file in sorted_files:
        output_file.write(bgp_file + "\n")

    output_file.close()

if __name__ == "__main__":
    list_files()
