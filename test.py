#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from time import time
from file import FileReader
from threading import Thread

def run_speed_test(filename):
    start = time()
    FileReader(filename)
    end = time()
    print("Time taken for " + filename + " was " + str(end - start))

def thread_test(filenames):
    for i in range(len(filenames)):
        t = Thread(target=run_speed_test, args=(filenames[i]))
        t.start()

start = "2001.10/RIBS/rib.20011026."
tests = [start+"1648.bz2",start+"1848.bz2",start+"2048.bz2",start+"2248.bz2"]
thread_test(tests)

"""        
run_speed_test("2001.10/RIBS/rib.20011026.1648.bz2")
run_speed_test("2001.10/RIBS/rib.20011026.1848.bz2")
run_speed_test("2001.10/RIBS/rib.20011026.2048.bz2")
run_speed_test("2001.10/RIBS/rib.20011026.2248.bz2")

run_speed_test("2014.06/RIBS/rib.20140601.0000.bz2")
run_speed_test("2014.06/RIBS/rib.20140601.0200.bz2")
run_speed_test("2014.06/RIBS/rib.20140601.0400.bz2")
run_speed_test("2014.06/RIBS/rib.20140601.0600.bz2")
"""