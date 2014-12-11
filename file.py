#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from subprocess import Popen, PIPE
from shlex import split
from threading import Lock
from sys import version_info
from os import walk
from re import compile

if version_info >= (3,0):
    from io import StringIO
else:
    from StringIO import StringIO

def get_bgp_files_in(dir):
    available_files = []
    walker = walk(dir)
    
    for file_data in walker:
        directory = file_data[0]
        filenames = file_data[2]
        
        for name in filenames:
            if is_valid_bgp_filename(name):
                available_files.append(dir + "/" + name)
                
    return available_files

def is_valid_bgp_filename(name):
    matcher = compile("rib.\d+.\d+.bz2")
    return matcher.match(name) is not None

        
class BGPDumpExecutor():
    def __init__(self, file_path):
        self.args     = split("bgpdump -m " + file_path)
        self.lock     = Lock()
        self.links    = set()
        self.ip_addrs = {}
        
        self.__run_executer()
        
    def __run_executer(self):
        with self.lock:
            proc = Popen(self.args, stdout=PIPE)
            stdout, stderr = proc.communicate()
            
            for line in stdout:
                self.__parse_line(line)
    
    def __parse_line(self, line):
        try:
            ip = line.split("|")[5].split("/")[0]
        except:
            ip = line.split("|")[5]
            
        hops = line.split("|")[6].split(" ")
        last_asys = self.__add_to_links([AS for AS in hops if not "{" in AS])
        self.ip_addrs[last_asys] = ip
        
    def __add_to_links(self, as_path):
        counter = 1
        
        while counter < len(as_path):
            if int(as_path[counter-1]) > int(as_path[counter]):
                self.links.add((as_path[counter], as_path[counter-1]))
            else:
                self.links.add((as_path[counter-1], as_path[counter]))
                
            counter += 1
            
        return int(as_path[-1])
    
    def get_ip_addresses(self):
        with self.lock:
            return self.ip_addrs
            
    def get_connections(self):
        with self.lock:
            return self.links