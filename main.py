#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from graphs import RingGraph, StaggeredRingGraph
from atlas_map import AtlasMap
from file import *
from chrono_atlas_map import ChronologicalAtlasMap
import logging

def bgp_thread(path):
    bgp_dump = BGPDumpExecutor(path)
    bgp_dumps[path] = bgp_dump
    print(path + " has completed")

logging.basicConfig(format="%(asctime)s %(message)s", filename="log.out")

all_files = get_bgp_files_under_directory("/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/")
files_to_use = []
bgp_dumps = {}

for year in range(2001, 2015):
    for month in range(1,13):
        date = str(year) + str(month).zfill(2)
        
        for bgp_file in all_files:
            if date in bgp_file:
                files_to_use.append(bgp_file)
                break
                
                

threads_in_use = []

for bgp_file in files_to_use:
    thr = Thread(target=bgp_thread, args=(bgp_file,))
    thr.start()
    threads_in_use.append(thr)
    
for thr in threads_in_use:
    thr.join()
    
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