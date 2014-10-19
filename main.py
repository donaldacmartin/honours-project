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

def get_path_from_line(line):
    try:
        return line.split("|")[6]
    except:
        return None
    
data = split_file_into_lines(read_file("/home/1101795m/output.out"))
print("Data read in successfully")

paths = []

for line in data:
    path = get_path_from_line(line)
    
    if path is not None:
        paths.append(path)
    
print("Paths extracted successfully")
print(str(len(paths)) + " paths found")

nodes = {}

for path in paths:
    try:
        hops = path.split(" ")
        
        if "{" in hops[-1]:
            del hops[-1]
        
        counter = 0
        while counter < len(hops):
            hop = int(hops[counter])
            
            if hop not in nodes:
                nodes[hop] = []
                
            if counter + 1 < len(hops):
                nodes[hop].append(int(hops[counter + 1]))
                
            if counter - 1 > 0:
                nodes[hop].append(int(hops[counter - 1]))
        
            counter += 1
    except:
        print("Encountered a problem with " + path)
            
print("Data sorted")