#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from subprocess import Popen
from shlex import split
from tempfile import NamedTemporaryFile
from threading import Lock

class FileReader():
    def __init__(self, filename):
        COMMAND = "bgpdump -m "
        PATH = "/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/"
        self.temp_file = NamedTemporaryFile()
        self.args = split(COMMAND + PATH + filename)
        self.lock = Lock()
        self.read_binary_into_ascii()
        self.nodes = {}
        
    def read_binary_into_ascii(self):
        with self.lock:
            p = Popen(self.args, stdout=self.temp_file)
            p.communicate()
            self.split_into_paths()
            
    def strip_invalid_entries(hops):
        if "{" in hops[-1]:
            del hops[-1]
        
        return hops
    
    def add_connection(self, node1, node2):
        if node1 not in self.nodes:
            self.nodes[node1] = []
        
        if node2 not in self.nodes[node1]:
            self.nodes[node1].append(node2)
    
    def append_to_nodes(self, hops):
        counter = 0
        
        while counter < len(hops):
            this_node = int(hops[counter])
            
            if counter + 1 < len(hops):
                self.add_connection(this_node, int(hops[counter + 1]))
                
            if counter - 1 > 0:
                self.add_connection(this_node, int(hops[counter - 1]))
                
            counter += 1
    
    def split_into_paths(self, data):
        self.temp_file.seek(0)
        data = self.temp_file.readline()
        
        while data != "" and data is not None:
            path = data.split("|")[6]
            hops = self.strip_invalid_entries(path.split(" "))
            self.append_to_nodes(hops)
            
    def get_entry(self, num):
        return self.nodes[num]
            
f = FileReader("2001.10/RIBS/rib.20011026.1648.bz2")
print(f.get_entry(1))