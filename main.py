#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from file import BGPDumpExecutor

filenames = ["bgpdata/2001.10/RIBS/rib.20011031.2234.bz2"]

for file in filenames:
    f = BGPDumpExecutor(file).get_connections()

    print("Completed Anaylsis of " + file)
    print("Number of connections: " + str(len(f)))