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
        read_binary_into_ascii()
        
    def read_binary_into_ascii(self):
        with self.lock:
            p = Popen(args, stdout=self.temp_file)
            self.temp_file.seek(0)
            
    def read_line(self):
        with self.lock:
            return self.temp_file.readline()
            
f = FileReader("2001.10/RIBS/rib.20011026.1648.bz2")
print(f.read_line())