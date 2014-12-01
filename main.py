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
gp = RingGraph(52400, 36800)

for cxn in connections:
    gp.add_link(cxn[0], cxn[1])
    
gp.draw_graph()