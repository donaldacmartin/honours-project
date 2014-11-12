#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

import time
from file import BGPDumpExecutor
from graph import NetworkGraph

start = time.time()

def write_output(text):
	with open("test.out", "a") as file:
		file.write(text + " - " + str(time.time() - start) + "\n")

write_output("Starting")

file = "bgpdata/2014.06/RIBS/rib.20140630.2200.bz2"
write_output("BGP Dump Extraction")

as_links = BGPDumpExecutor(file2).get_connections()
write_output("Links Extracted")

NetworkGraph(as_links, 3000000000, "3000000000.png")
write_output("Graph Created")