#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

import logging

from graphs.chrono_atlas_map import ChronologicalAtlasMap
from utilities.bgp import BGPDumpExecutor
from utilities.threads import run_bgp_dump

base_dir = "/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/"

files = [base_dir + "2001.10/RIBS/rib.20011027.0849.bz2",
         base_dir + "2003.10/RIBS/rib.20031021.1648.bz2"]

bgp_dumps = run_bgp_dump(files)

for i in range(1, len(files)):
    prev_file = files[i-1]
    curr_file = files[i]
    
    prev_cxns = bgp_dumps[prev_file].as_connections
    curr_cxns = bgp_dumps[curr_file].as_connections
    
    prev_addr = bgp_dumps[prev_file].as_to_ip_address
    curr_addr = bgp_dumps[curr_file].as_to_ip_address
    
    chrono = ChronologicalAtlasMap(1920,1080, prev_cxns, curr_cxns, prev_addr, curr_addr)
    chrono.save("test-chrono" + str(i) + ".png")