#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from PIL.Image import open
from os import listdir
from sys import argv
from utilities.images2gif import writeGif

def create_gifs(filename):
    files  = sorted((f for f in os.listdir("temp") if f.endswith(".png")))
    images = [open(f) for f in files]

    writeGif(filename, images, duration=0.5)

if __name__ == "__main__":
    create_gifs(argv[1])
