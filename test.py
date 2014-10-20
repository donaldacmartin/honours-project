#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from time import time
from file import FileReader

def run_speed_test(filename):
    start = time()
    FileReader(filename)
    end = time()
    print("Time taken for " + filename + " was " + str(end - start))

run_speed_test("2001.10/RIBS/rib.20011026.1648.bz2")