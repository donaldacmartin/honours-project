#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from os import listdir
from subprocess import check_output, STDOUT

PATH = "/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/"
CMD  = "bgpdump -m <filename>"

as_paths = {}

def is_bgpdump_installed():
    try:
        output = check_output("bgpdump", shell=True, stderr=STDOUT)
    except Exception, e:
        output = str(e.output)
    
    return "bgpdump version" in output
    
def get_all_folders():
    available_months = listdir(PATH)
    dump_path = PATH + available_months[0] + "/RIBS/"
    available_dumps  = listdir(dump_path)
    output = dump_path + available_dumps[0]
    return output

def to_ascii(cmd):
    try:
        output = check_output(cmd, shell=True, stderr=STDOUT)
    except Exception, e:
        output = str(e.output)
    
    lines = output.split("\n")
    
    for line in lines:
        try:
            path = line.split("|")[6]
            hops = path.split(" ")
            
            if hops[-1] in as_paths:
                as_paths[hops[-1]].append(hops)
            else:
                as_paths[hops[-1]] = [hops]
        except:
            print("Unable to get line")

to_ascii("bgpdump -m " + get_all_folders())

while True:
    k = input()
    print(as_paths(k))