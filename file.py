#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from subprocess import Popen, PIPE
from shlex import split
from sys import version_info
from os import walk
from re import compile

if version_info >= (3,0):
    from io import StringIO
else:
    from StringIO import StringIO

"""
BGPDumpExecutor

A class that acts as an interface to the BGPDump tool. Takes a filename and
generates a set of connections between autonomous systems (each link is stored
as a tuple containing the lower AS number then the larger AS number). A set is
used in order to save memory and avoid duplication. Also generates a lookup
table for AS numbers to IP addresses.
"""
    
class BGPDumpExecutor():
    def __init__(self, file_path):
        self.args = split("bgpdump -m " + file_path)
        
        self.connections  = set()
        self.ip_addresses = {}
        
        self.__run_executer()
        
    def __run_executer(self):
        proc   = Popen(self.args, stdout=PIPE)
        stdout = proc.communicate()[0]
        lines  = [line for line in stdout.split("\n") if line != " " and line != ""]
        
        for line in lines:
            self.__parse_line(line)
    
    def __parse_line(self, line):
        ip_address = self.__get_ip_address_from_line(line)
        
        bgp_hops = line.split("|")[6].split(" ")
        as_path  = [int(AS) for AS in bgp_hops if not "{" in AS]
        
        self.__add_as_path_to_connections(as_path)
        self.ip_addresses[as_path[-1]] = ip_address
        
    def __get_ip_address_from_line(self, line):
        try:
            ip_address = line.split("|")[5]
            
            if "/" in ip_address:
                ip_address = ip_address.split("/")[0]
                
            return ip_address
        except:
            print(line)
    
    def __add_as_path_to_connections(self, as_path):
        for i in range(1, len(as_path)):
            prev_asys = as_path[i-1]
            this_asys = as_path[i]
            
            link = (min(prev_asys, this_asys), max(prev_asys, this_asys))
            self.connections.add(link)
            
def get_bgp_files_under_directory(dir):
    bgp_regex_matcher = compile("rib.\d+.\d+.bz2")
    available_files   = []
    walker = walk(dir)
    
    for file_data in walker:
        directory = file_data[0]
        filenames = file_data[2]
        
        for name in filenames:
            if bgp_regex_matcher.match(name) is not None:
                available_files.append(directory + "/" + name)
                
    return available_files