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
        self.buffer = None
        self.__run_executer()
        
    def __run_executer(self):
        with self.lock:
            std_out = Popen(self.args, stdout=PIPE).communicate()[0]
            self.buffer = StringIO(std_out)
    
    def get_output(self):
        with self.lock:
            return self.buffer
            
class BGPDumpParser():
    def __init__(self, buffer):
        self.lock = Lock()
        self.cxn_list = []
        self.__parse_lines(buffer)
        
    def __parse_lines(self, buffer):
        with self.lock:
            line = buffer.readline()
            
            while line != "" and line is not None:
                hops = line.split("|")[6].split(" ")
                # print("Hops: " + str(len(hops)))
                # print("List: " + str(len([AS for AS in hops if not "{" in AS])))
                self.cxn_list.append([AS for AS in hops if not "{" in AS])
                line = buffer.readline()
                
    def get_list_of_connections(self):
        with self.lock:
            return self.cxn_list
            
class ASIndex():
    def __init__(self, connection_list):
        self.lock = Lock()
        self.index = {}
        
    def __convert_list_to_dictionary(self, connection_list):
        with self.lock:
            for as_path in connection_list:
                print("AS Path: " + str(len(as_path)))
                self.__add_as_path_to_dictionary(as_path)
    
    def __add_as_path_to_dictionary(self, as_path):
        counter = 0
        
        while counter < len(as_path):
            if counter > 0:
                self.__add_connection(as_path[counter], as_path[counter - 1])
                
            if counter < len(as_path - 1):
                self.__add_connection(as_path[counter], as_path[counter + 1])
                
            counter += 1
                
    def __add_connection(self, asys1, asys2):
        if asys1 not in self.index:
            self.index[asys1] = []
        
        if asys2 not in self.index:
            self.index[asys2] = []
            
        self.index[asys1].append(asys2)
        self.index[asys2].append(asys1)
    
    def get_index(self):
        with self.lock:
            return self.index
            
def get_file_contents(file_path):
    buffer = BGPDumpExecuter(file_path).get_output()
    connection_list = BGPDumpParser(buffer).get_list_of_connections()
    return ASIndex(connection_list).get_index()