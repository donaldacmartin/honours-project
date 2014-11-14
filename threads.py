#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from file import *
from threading import Thread
from graph import NetworkGraph

def master_method():
    files = FileFinder("/nas05/users/csp/routing-data/").get_files()
    files_for_date = []
    
    output = NetworkGraph("super-out.png")
    threads_list = []
    counter = 0
    
    for f in files:
        if f.get_date() == "20101227":
            threads_list.append(Thread(target=worker_method, args=(f.get_path(), output)))
            counter += 1
            
    for worker in threads_list:
        worker.start()
    
    while counter > 0:
        for worker in threads_list:
            if not worker.isAlive():
                counter -= 1
                
    output.draw()
            
def worker_method(filename, global_graph):
    connections = BGPDumpExecutor(filename).get_connections()
    global_graph.add_edges(connections)

thread_master = Thread(target=master_method)