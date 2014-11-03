#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

sys.path.append("/home/1101795m/local/lib/python/")

from file import BGPDumpExecutor
from graph import NetworkGraph

file     = "bgpdata/2001.10/RIBS/rib.20011031.2234.bz2"
as_links = BGPDumpExecutor(file).get_connections()
NetworkGraph(as_links)