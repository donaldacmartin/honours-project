#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from subprocess import Popen, PIPE
from shlex import split
from threading import Lock
from StringIO import StringIO # from io import StringIO (Python 3)

class BGPDumpExecutor():
    """
    BGPDumpExecuter creates an abstraction layer, that runs the C-based bgpdump
    tool to convert binary MRT data into ASCII. The links between ASs are
    extracted and placed into a set of tuples for graphing.
    """
    def __init__(self, file_path):
        """
        Initialisation: store command to execute bgpdump and a path to the root
        directory of BGP files. Create a lock to avoid accessing data structure
        prematurely.
        """
        command = "bgpdump -m "
        root_path = "/nas05/users/csp/routing-data/archive.routeviews.org/"
         
        self.args = split(command + root_path + file_path)
        self.lock = Lock()
        self.links = set()
        self.__run_executer()
        
    def __run_executer(self):
        """
        Run the bgpdump tool as a subprocess and pipe the stdout line-by-line
        into the parser.
        """
        with self.lock:
            proc = Popen(self.args, stdout=PIPE)
            
            for line in iter(proc.stdout.readline, ""):
                self.__parse_line(line)
    
    def __parse_line(self, line):
        """
        From the line, extract the 5th column (AS paths) and convert to a list.
        Remove any AS sets (these are already included in the list.
        """
        hops = line.split("|")[6].split(" ")
        self.__add_to_links([AS for AS in hops if not "{" in AS])
        
    def __add_to_links(self, as_path):
        """
        Convert list of AS hops into tuples. Store the tuple in the set, with
        the smaller number first (avoids data duplication).
        """
        counter = 1
        
        while counter < len(as_path):
            if int(as_path[counter-1]) > int(as_path[counter]):
                self.links.add((as_path[counter], as_path[counter-1]))
            else:
                self.links.add((as_path[counter-1], as_path[counter]))
                
            counter += 1
        
    def get_connections(self):
        """
        Return the output only if the bgpdump tool isn't currently analysing
        data (mutex lock).
        """
        with self.lock:
            return self.links