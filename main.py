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

base_dir       = "/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/"
dir = base_dir + "2001.10/RIBS/rib.20011027.0849.bz2"
"""
bgp_files      = get_bgp_files_in(base_dir)
files_to_parse = []
bgp_dumps      = []

for year in range(2001, 2002):
    for month in range(10, 12):
        year_date = "rib." + str(year) + str(month).zfill(2)
        
        for bgp_file in bgp_files:
            if year_date in bgp_file:
                files_to_parse.append(bgp_file)
                break

for bgp_file in files_to_parse:
    bgp_dumps.append(BGPDumpExecutor(bgp_file))
    
for i in range(1, len(bgp_dumps)):
    prev_dump = bgp_dumps[i-1]
    this_dump = bgp_dumps[i]
    
    ip_addresses = this_dump.get_ip_addresses()
    
    connections      = this_dump.get_connections()
    prev_connections = prev_dump.get_connections()
    
    connections_new       = connections.difference(prev_connections)
    connections_removed   = prev_connections.difference(connections)
    connections_unchanged = connections.intersection(prev_connections)
    
    chrono_atlas = ChronologicalAtlasMap("map" + str(i) + ".png", 20000, 10000)
    
    for auto_sys in ip_addresses:
        chrono_atlas.add_auto_sys_ip(auto_sys, ip_addresses[auto_sys])
        
    for cxn in connections_new:
        chronoatlas.add_new_link(cxn[0], cxn[1])
    
    for cxn in connections_removed:
        chronoatlas.add_removed_link(cxn[0], cxn[1])
        
    for cxn in connections_new:
        chronoatlas.add_unchanged_link(cxn[0], cxn[1])
        
    chrono_atlas.draw_graph()
    
"""
bgp_dump = BGPDumpExecutor(dir)

#ring        = RingGraph("ring-graph.png", 20000, 20000)
#staggered   = StaggeredRingGraph("staggered-graph.png", 20000, 20000)
atlas       = AtlasMap(20000, 10000)
#chronoatlas = ChronologicalAtlasMap("chrono-atlas.png", 20000, 10000)

counter = 0

for auto_sys in bgp_dump.ip_addresses:
    counter += 1
    print("AS: " + str(counter))
    atlas.add_auto_sys_ip(auto_sys, bgp_dump.ip_addresses[auto_sys])
    
counter = 0

for cxn in bgp_dump.connections:
    counter += 1
    print("CN: " + str(counter))
    atlas.add_link(cxn[0], cxn[1])

print("Drawing")
atlas.draw_graph()
atlas.save_graph("new-atlas-map.png")