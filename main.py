#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from graphs import RingGraph, StaggeredRingGraph
from atlas_map import AtlasMap
from file import *
from chrono_atlas_map import ChronologicalAtlasMap

"""
import pickle
pickle.dump(connections, open("sampleset", "wb"))
connections = pickle.load(open("sampleset", "rb"))
"""

dir = "/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/2001.10/RIBS/rib.20011026.1648.bz2"

bgp_dump     = BGPDumpExecutor(dir)
ip_addresses = bgp_dump.get_ip_addresses()
connections  = bgp_dump.get_connections()

#ring        = RingGraph("ring-graph.png", 20000, 20000)
#staggered   = StaggeredRingGraph("staggered-graph.png", 20000, 20000)
#atlas       = AtlasMap("atlas-map.png", 20000, 10000)
chronoatlas = ChronologicalAtlasMap("chrono-atlas.png", 20000, 10000)

for auto_sys in ip_addresses:
    chronoatlas.add_auto_sys_ip(auto_sys, ip_addresses[auto_sys])

switch = 0
    
for cxn in connections:
    if switch == 0:
        switch = 1
        chronoatlas.add_new_link(cxn[0], cxn[1])
    elif switch == 1:
        switch = 2
        chronoatlas.add_removed_link(cxn[0], cxn[1])
    else:
        switch = 0
        chronoatlas.add_unchanged_link(cxn[0], cxn[1])

print("Drawing")
#ring.draw_graph()
#staggered.draw_graph()
chronoatlas.draw_graph()