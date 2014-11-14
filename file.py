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

class FileFinder():
    def __init__(self, root_directory):
        self.walker = walk(root_directory)
        self.__get_file_info()
        
    def __get_file_info(self):
        self.available_files = []
        
        for file_data in self.walker:
            directory = file_data[0]
            filenames = file_data[2]
            
            for name in filenames:
                self.available_files.append(BGPFile(name, directory))
                
    def get_files(self):
        return self.available_files

class BGPFile():
    def __init__(self, name, dir):
        self.name = name
        self.directory = dir
        self.__parse_name()
        
    def __parse_name(self):
        matcher = compile("rib.\d+.\d+.bz2")
        
        if matcher.match(self.name) is not None:
            self.date = self.name.split(".")[1]
            self.time = self.name.split(".")[2]
            
    def get_name(self):
        return self.name
        
    def get_directory(self):
        return self.directory
    
    def get_date(self):
        return self.date
        
    def get_time(self):
        return self.time
        
class BGPDumpExecutor():
    def __init__(self, file_path):
        command = "bgpdump -m "
        root_path = "/nas05/users/csp/routing-data/archive.routeviews.org/"
         
        self.args = split(command + root_path + file_path)
        self.lock = Lock()
        self.links = set()
        self.__run_executer()
        
    def __run_executer(self):
        with self.lock:
            proc = Popen(self.args, stdout=PIPE)
            
            for line in iter(proc.stdout.readline, ""):
                self.__parse_line(line)
    
    def __parse_line(self, line):
        hops = line.split("|")[6].split(" ")
        self.__add_to_links([AS for AS in hops if not "{" in AS])
        
    def __add_to_links(self, as_path):
        counter = 1
        
        while counter < len(as_path):
            if int(as_path[counter-1]) > int(as_path[counter]):
                self.links.add((as_path[counter], as_path[counter-1]))
            else:
                self.links.add((as_path[counter-1], as_path[counter]))
                
            counter += 1
        
    def get_connections(self):
        with self.lock:
            return self.links