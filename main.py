#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from EasyGraph import *
from file import *
import pickle

"""
connections = BGPDumpExecutor("/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/2001.10/RIBS/rib.20011026.1648.bz2").get_connections()
pickle.dump(connections, open("sampleset", "wb"))
"""

connections = pickle.load(open("sampleset", "rb"))
#ring        = RingGraph(20000, 20000)
staggered   = StaggeredRingGraph(40000, 40000)

for cxn in connections:
    #ring.add_link(cxn[0], cxn[1])
    staggered.add_link(cxn[0], cxn[1])
    
#ring.draw_graph()
staggered.draw_graph()