#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from utilities.file_search import get_bgp_binaries_in
from utilities.images2gif import writeGif
from graphs.chrono_atlas_map import ChronologicalAtlasMap
from multiprocessing import Process, Semaphore, Manager, Lock
from utilities.bgp import BGPDumpExecutor
from time import time
from utilities.process_pool import ProcessPool

def generate_monthly_diff():
    files          = __get_list_of_files()
    processes      = []
    manager        = Manager()
    bgp_dumps      = manager.dict()
    asys_coords    = manager.dict()
    
    start = time()
    
    print("Starting BGPing")
    
    proc_pool      = ProcessPool(30)
    
    for bgp_file in files:
        args = (bgp_file, bgp_dumps,)
        proc_pool.add_job(__bgp_process, args)
        
    proc_pool.run()
    proc_pool.join()
    
    print("Finished BGPing, now graphing")
    
    for i in range(1, len(files)):
        prev_file = files[i-1]
        curr_file = files[i]
        
        args = (prev_file, curr_file, bgp_dumps, asys_coords, i,)
        proc_pool.add_job(__chrono_map_process, args)
        
    proc_pool.run()
    proc_pool.join()
    
    end = time()
    print("Completed " + str(len(files)) + " in " + str(end - start) + "s")
    
def __get_list_of_files():
    base_dir  = "/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/"
    all_files = get_bgp_binaries_in(base_dir)
    months    = []
    
    for year in range(2001, 2003):
        for month in range(1, 13):
            filename = __filter_a_file(all_files, month, year)
            
            if filename is not None:
                months.append(filename)
    
    return months
    
def __filter_a_file(files, month, year):
    name_key = "rib." + str(year) + str(month).zfill(2)
    
    for bgp_file in files:
        if name_key in bgp_file:
            return bgp_file
            
    return None

def __bgp_process(filename, bgp_dumps):
    bgp = BGPDumpExecutor(filename)
    bgp_dumps[filename] = bgp
    
def __chrono_map_process(prev_filename, curr_filename, bgp_dumps, asys_coords, counter):
    prev_cxns = bgp_dumps[prev_filename].as_connections
    curr_cxns = bgp_dumps[curr_filename].as_connections
    
    prev_addr = bgp_dumps[prev_filename].as_to_ip_address
    curr_addr = bgp_dumps[curr_filename].as_to_ip_address
    
    chrono = ChronologicalAtlasMap(20000,10000, prev_cxns, curr_cxns, prev_addr, curr_addr, asys_coords)
    chrono.save(str(counter) + ".png")