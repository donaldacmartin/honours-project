#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from utilities.bgp import BGPDumpExecutor

def bgp_dump_thread(file_path, bgp_database):
    bgp = BGPDumpExecutor(file_path)
    bgp_database[file_path] = bgp
    
def run_bgp_dump(files, max_threads):
    threads = []
    
    bgp_file = files.pop()
    Thread(target=bgp_dump_thread, )