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
        self.args = split("bgpdump -m " + file_path)
        
        self.connections  = set()
        self.ip_addresses = {}
        
        self.__run_executer()
        
    def __run_executer(self):
        proc = Popen(self.args, stdout=PIPE)
        stdout, stderr = proc.communicate()
        
        lines = stdout.split("\n")
        
        for line in lines:
            if line != "":
                self.__parse_line(line)
    
    def __parse_line(self, line):
        ip_address = self.__get_ip_address_from_line(line)
        
        bgp_hops  = line.split("|")[6].split(" ")
        as_path   = [int(AS) for AS in bgp_hops if not "{" in AS]
        
        self.__add_as_path_to_connections(as_path)
        self.ip_addresses[as_path[-1]] = ip_address
        
    def __get_ip_address_from_line(self, line):
        ip_address = line.split("|")[5]
        
        if "/" in ip_address:
            ip_address = ip_address.split("/")[0]
            
        return ip_address
    
    def __add_as_path_to_connections(self, as_path):
        for i in range(1, len(as_path)):
            prev_asys = as_path[i-1]
            this_asys = as_path[i]
            
            link = (min(prev_asys, this_asys), max(prev_asys, this_asys))
            self.connections.add(link)