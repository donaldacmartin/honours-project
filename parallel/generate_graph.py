#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from sys import argv
from pickle import load
from graphs.atlas.chrono_atlas_map import ChronoAtlasMap

def generate_graphs(filename1, filename2):
    bgp1 = unpickle_dump("temp/" + filename1.replace("/", "_"))
    bgp2 = unpickle_dump("temp/" + filename2.replace("/", "_"))

    chrono = ChronoAtlasMap(1920, 1080, bgp1, bgp2)

    title = get_title_from_filename(filename1)
    chrono.draw_text(title)

    chrono.save("temp/map" + filename1.replace("/", "_") + ".png")

def unpickle_dump(filename):
    pickle_file = open(filename, "rb")
    bgp_file = load(pickle_file)

    pickle_file.close()
    return bgp_file

def get_title_from_filename(filename):
    date_start = filename.find("rib.") + 4
    year       = filename[date_start:date_start+8]
    month      = int(filename[date_start+8:date_start+10])

    months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep",
              "Oct", "Nov", "Dec"]

    return months[month-1] + " " + year

if __name__ == "__main__":
    generate_graphs(argv[1], argv[2])
