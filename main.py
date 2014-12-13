#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

import logging

from graphs.ring_graph import RingGraph
from graphs.atlas_map import AtlasMap
from graphs.chrono_atlas_map import ChronologicalAtlasMap
from utilities.bgp import BGPDumpExecutor

bgp1 = BGPDumpExecutor("/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/2001.10/RIBS/rib.20011027.0849.bz2")
bgp2 = BGPDumpExecutor("/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/2003.10/RIBS/rib.20031021.1648.bz2")

ring  = RingGraph(1080, 1920, bgp1.as_connections)
ring.save("test-ring.png")

atlas = AtlasMap(1080, 1920, bgp.as_connections, bgp1.as_to_ip_address)
atlas.save("test-atlas.png")

chrono = ChronologicalAtlasMap(1080,1920, bgp1.as_connections, bgp2.as_connections, bgp1.as_to_ip_address, bgp2.as_to_ip_address)
chrono.save("test-chrono.png")