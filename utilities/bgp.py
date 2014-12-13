#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from subprocess import Popen, PIPE
from shlex import split
from sys import version_info
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
        
        self.as_connections   = set()
        self.as_to_ip_address = {}
        
        self.__run_executer()
        
    def __run_executer(self):
        proc  = Popen(self.args, stdout=PIPE)
        pipe  = proc.communicate()[0]
        lines = [line for line in pipe.split("\n") if line != "" and line != " "]
        
        for line in lines:
            self.__parse_line(line)
    
    def __parse_line(self, line):
        ip_address = self.__get_ip_address(line)
        asys_hops  = line.split("|")[6].split(" ")
        asys_path  = [int(AS) for AS in asys_hops if self.__is_valid_asys(AS)]
        
        self.as_to_ip_address[as_path[-1]] = ip_address
        self.__add_as_path_to_connections(as_path)
        
    def __is_valid_asys(self, asys):
        if "(" in asys or ")" in asys:
            return False
            
        if "{" in asys or "}" in asys:
            return False
            
        return True
        
    def __get_ip_address(self, line):
        ip_address = line.split("|")[5]
        
        if "/" in ip_address:
            ip_address = ip_address.split("/")[0]
            
        return ip_address
    
    def __add_as_path_to_connections(self, as_path):
        for i in range(1, len(as_path)):
            prev_asys = as_path[i-1]
            this_asys = as_path[i]
            
            link = (min(prev_asys, this_asys), max(prev_asys, this_asys))
            self.as_connections.add(link)