#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from subprocess import Popen, PIPE
from shlex import split
from threading import Lock
from StringIO import StringIO # from io import StringIO (Python 3)

class BGPDumpExecuter():
    def __init__(self, file_path):
        command = "bgpdump -m "
        root_path = "/nas05/users/csp/routing-data/archive.routeviews.org/"
         
        self.args = split(command + root_path + file_path)
        self.lock = Lock()
        self.parser = BGPDumpParser()
        self.__run_executer()
        
    def __run_executer(self):
        with self.lock:
            proc = Popen(self.args, stdout=PIPE).communicate()[0]
            
            for line in iter(proc.stdout.readline, ""):
                self.parser.parse_line(line)
    
    def get_output(self):
        with self.lock:
            return self.parser.get_connections()
            
class BGPDumpParser():
    def __init__(self):
        self.index = {}
        
    def parse_line(self, line):
        hops = line.split("|")[6].split(" ")
        self.__add_to_dictionary([AS for AS in hops if not "{" in AS])
                
    def __add_to_dictionary(self, as_path):
        counter = 0
        
        while counter < len(as_path):
            if counter > 0:
                self.__add_connection(as_path[counter], as_path[counter - 1])
                
            if counter < len(as_path) - 1:
                self.__add_connection(as_path[counter], as_path[counter + 1])
                
            counter += 1
    
    def __add_connection(self, asys1, asys2):
        if asys1 not in self.index:
            self.index[asys1] = set()
        
        if asys2 not in self.index:
            self.index[asys2] = set()
            
        self.index[asys1].add(asys2)
        self.index[asys2].add(asys1)
        
    def get_connections(self):
        with self.lock:
            return self.index
            
def get_file_contents(file_path):
    return BGPDumpExecuter(file_path).get_output()