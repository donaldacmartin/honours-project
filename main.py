#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from utilities.bgp import BGPDumpExecutor

from graphs.atlas.atlas_map import AtlasMap, EUROPE
from graphs.atlas.chrono_atlas_map import ChronoAtlasMap
from graphs.ring.ring_graph import RingGraph
from utilities.process_pool import ProcessPool

base = "/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/"

bgp1 = BGPDumpExecutor(base + "2001.10/RIBS/rib.20011026.1648.bz2")
bgp2 = BGPDumpExecutor(base + "2002.10/RIBS/rib.20021026.1517.bz2")

"""
a = AtlasMap(1920, 1080, bgp1)
a.save("atlas-no-limits.png")
"""
"""
b = AtlasMap(1920, 1080, bgp1, EUROPE)
b.save("atlas-limits.png")
"""

c = ChronoAtlasMap(1920, 1080, bgp1, bgp2)
c.save("chrono.png")
"""
r = RingGraph(1080, bgp1)
r.save("ring.png")
"""
