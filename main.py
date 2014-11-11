#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

import time
from file import BGPDumpExecutor
from graph import NetworkGraph

def write_output(counter, timer):
	with open("test.out", "a") as file:
		file.write(str(counter) + str(timer) + "\n")

file     = "bgpdata/2001.10/RIBS/rib.20011031.2234.bz2"
file2	 = "bgpdata/2014.06/RIBS/rib.20140630.2200.bz2"
as_links = BGPDumpExecutor(file2).get_connections()

test_cases = [3000000000]

for test in test_cases:
	start = time.time()
	NetworkGraph(as_links, test, str(test) + ".png")
	end = time.time()
	write_output(test, end-start)
