#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from threading import Thread
from chrono_atlas_map import ChronologicalAtlasMap
from file import *

def bgpdump_thread(path):
    bgp_dump = BGPDumpExecutor(path)
    bgp_dumps[path] = bgp_dump
    
def graph_producer_thread(path1, path2, filename):
    chrono = ChronologicalAtlasMap(filename, 20000, 10000)
    
    prev_dump = bgp_dumps[path1]
    curr_dump = bgp_dumps[path2]
    
    for auto_sys in prev_dump.ip_addresses:
        chrono.add_auto_sys_ip(auto_sys, prev_dump.ip_addresses[auto_sys])
        
    for auto_sys in curr_dump.ip_addresses:
        chrono.add_auto_sys_ip(auto_sys, curr_dump.ip_addresses[auto_sys])
    
    new_connections = curr_dump.connections.difference(prev_dump.connections)
    old_connections = prev_dump.connections.difference(curr_dump.connections)
    sme_connections = curr_dump.connections.intersection(prev_dump.connections)
    
    for (start, end) in new_connections:
        chrono.add_new_link(start, end)
        
    for (start, end) in old_connections:
        chrono.add_removed_link(start, end)
        
    for (start, end) in unchanged_connections:
        chrono.add_new_link(start, end)
        
    chrono.draw_graph()
    
all_files = get_bgp_files_under_directory("/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/")
files_to_use = []
bgp_dumps = {}

for year in range(2002, 2015):
    date = "rib." + str(year) + "01"
    
    for bgp_file in all_files:
        if date in bgp_file:
            files_to_use.append(bgp_file)
            break

threads_in_use = []
threads_in_use2 = []

for bgp_file in files_to_use:
    thr = Thread(target=bgpdump_thread, args=(bgp_file,))
    thr.start()
    threads_in_use.append(thr)
    
for thr in threads_in_use:
    thr.join()

for i in range(1, len(files_to_use), 2):
    path1 = files_to_use[i-1]
    path2 = files_to_use[i]
    fname = "map" + str(i) + ".png"
    
    thr = Thread(target=graph_producer_thread, args=(path1,path2,fname,))
    thr.start()
    threads_in_use2.append(thr)
    
for thr in threads_in_use2:
    thr.join()