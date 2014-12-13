#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from utilities.bgp import BGPDumpExecutor
from threading import Thread

def run_bgp_dump(files):
    threads   = []
    bgp_dumps = {}
    
    for bgp_file in files:
        thread = Thread(target=bgp_dump_thread, args=(bgp_file, bgp_dumps,))
        thread.start()
        threads.append(thread)
    
    __wait(threads)
    return bgp_dumps
    
def bgp_dump_thread(file_path, bgp_database):
    bgp = BGPDumpExecutor(file_path)
    bgp_database[file_path] = bgp

def __wait(threads):
    for thread in threads:
        thread.join()