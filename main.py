#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

"""
Will be useful later
from os import listdir
from subprocess import check_output, STDOUT

PATH = "/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/"
CMD  = "bgpdump -m <filename>"
"""

def read_file(filename):
    try:
        file = open(filename, "r")
        contents = file.read()
        file.close()
        return contents
    except:
        print("Error opening file " + filename)
        exit()
        
def split_file_into_lines(file_contents):
    return file_contents.split("\n")
    
data = split_file_into_lines(read_file("/home/1101795m/output.out"))
print("Data read in successfully")