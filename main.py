#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from graphs import RingGraph, StaggeredRingGraph
from atlas_map import AtlasMap
from file import *

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
atlas       = AtlasMap("atlas-map.png", 20000, 10000)

for auto_sys in ip_addresses:
    atlas.add_auto_sys_ip(auto_sys, ip_addresses[auto_sys])

for cxn in connections:
    #ring.add_link(cxn[0], cxn[1])
    #staggered.add_link(cxn[0], cxn[1])
    atlas.add_link(cxn[0], cxn[1])

#ring.draw_graph()
#staggered.draw_graph()
atlas.draw_graph()