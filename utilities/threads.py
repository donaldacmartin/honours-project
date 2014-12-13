#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from utilities.bgp import BGPDumpExecutor
from threading import Thread
from graphs.chrono_atlas_map import ChronologicalAtlasMap

def run_bgp_dump(files):
    threads   = []
    bgp_dumps = {}
    
    for bgp_file in files:
        thread = Thread(target=__bgp_dump_thread, args=(bgp_file, bgp_dumps,))
        thread.start()
        threads.append(thread)
    
    __wait(threads)
    return bgp_dumps
    
def generate_chrono_map(filenames, bgp_dumps):
    threads = []
    
    for i in range(1, len(filenames)):
        prev_dump = bgp_dumps[filenames[i-1]]
        curr_dump = bgp_dumps[filenames[i]]
        
        args = (prev_dump, curr_dump, str(i) + ".png",)
        thread = Thread(target=__generate_chrono_map_thread, args=args)
        thread.start()
        threads.append(thread)
        
    __wait(threads)
    
def __bgp_dump_thread(file_path, bgp_database):
    bgp = BGPDumpExecutor(file_path)
    bgp_database[file_path] = bgp

def __wait(threads):
    for thread in threads:
        thread.join()
        
def __generate_chrono_map_thread(bgp_dump1, bgp_dump2, name):
    prev_cxns = bgp_dump1.as_connections
    curr_cxns = bgp_dump2.as_connections
    
    prev_addr = bgp_dump1.as_to_ip_address
    curr_addr = bgp_dump2.as_to_ip_address
    
    chrono = ChronologicalAtlasMap(1920,1080, prev_cxns, curr_cxns, prev_addr, curr_addr)
    chrono.save(name)