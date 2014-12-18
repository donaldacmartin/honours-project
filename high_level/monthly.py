#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from utilities.threads import run_bgp_dump, generate_chrono_map
from utilities.file_search import get_bgp_binaries_in
from utilities.images2gif import writeGif
from graphs.chrono_atlas_map import ChronologicalAtlasMap
from multiprocessing import Process, Semaphore
from utilities.bgp import BGPDumpExecutor

def generate_monthly_diff():
    files       = __get_list_of_files()
    semaphores  = [Semaphore(2) for _ in range(len(files))]
    bgp_dumps   = {}
    asys_coords = {}
    
    for i in range(len(files)):
        args = (files[i], bgp_dumps, semaphores[i], i,)
        proc = Process(target=__bgp_process, args=args)
        proc.start()
        
    for i in range(1, len(files)):
        args = (files[i-1], files[i], semaphores[i-1], semaphores[i], bgp_dumps, asys_coords, i,)
        proc = Process(target=__chrono_map_process, args=args)
        proc.start()
    
def __get_list_of_files():
    base_dir  = "/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/"
    all_files = get_bgp_binaries_in(base_dir)
    months    = []
    
    
    for year in range(2001, 2002):
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

def __bgp_process(filename, bgp_dumps, semaphore, counter):
    semaphore.acquire()
    semaphore.acquire()
    
    print("Starting to get BGP for " + str(counter))
    
    bgp = BGPDumpExecutor(filename)
    bgp_dumps[filename] = bgp
    
    print("Finished BGP for " + str(counter))
    
    semaphore.release()
    semaphore.release()
    
def __chrono_map_process(prev_filename, curr_filename, prev_semaphore, curr_semaphore, bgp_dumps, asys_coords, counter):
    prev_semaphore.acquire()
    curr_semaphore.acquire()
    
    print("Starting to graph for " + str(counter))
    
    prev_cxns = bgp_dumps[prev_filename].as_connections
    curr_cxns = bgp_dumps[curr_filename].as_connections
    
    prev_addr = bgp_dumps[prev_filename].as_to_ip_address
    curr_addr = bgp_dumps[curr_filename].as_to_ip_address
    
    chrono = ChronologicalAtlasMap(20000,10000, prev_cxns, curr_cxns, prev_addr, curr_addr, asys_coords)
    chrono.save(str(counter) + ".png")
    
    print("Finished graph for " + str(counter))
    
    curr_semaphore.release()
    prev_semaphore.release()