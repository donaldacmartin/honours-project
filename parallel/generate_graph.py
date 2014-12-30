#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from sys import argv
from pickle import load
from graphs.atlas.chrono_atlas_map import ChronoAtlasMap

def generate_graphs(filename1, filename2):
    bgp1 = unpickle_dump(filename1)
    bgp2 = unpickle_dump(filename2)

    chrono = ChronoAtlasMap(1920, 1080, bgp1, bgp2)
    chrono.save("temp/map" + filename1 + ".png")

def unpickle_dump(filename):
    pickle_file = open("temp/" + filename, "rb")
    bgp_file = load(pickle_file)

    pickle_file.close()
    return bgp_file

if __name__ == "main":
    generate_graphs(argv[1], argv[2])
