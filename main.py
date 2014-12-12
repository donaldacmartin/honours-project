#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from graphs import RingGraph, StaggeredRingGraph
from atlas_map import AtlasMap
from file import *
from chrono_atlas_map import ChronologicalAtlasMap
import logging

logging.basicConfig(format="%(asctime)s %(message)s", filename="log.out")

bgp_dump1 = BGPDumpExecutor("/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/2001.10/RIBS/rib.20011027.0849.bz2")
bgp_dump2 = BGPDumpExecutor("/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/2003.10/RIBS/rib.20031027.1313.bz2")

chrono = ChronologicalAtlasMap("chrono.png",20000,10000)

for asys in bgp_dump2.ip_addresses:
    chrono.add_auto_sys_ip(asys, bgp_dump2.ip_addresses[asys])
    
new       = bgp_dump2.connections.difference(bgp_dump1.connections)
removed   = bgp_dump1.connections.difference(bgp_dump2.connections)
unchanged = bgp_dump1.connections.intersection(bgp_dump2.connections)

for (start,end) in new:
    chrono.add_new_link(start,end)
    
for (start,end) in removed:
    chrono.add_removed_link(start,end)
    
for (start,end) in unchanged:
    chrono.add_unchanged_link(start,end)
    
chrono.draw_graph()