#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from os import walk
from re import compile

"""
File Search

Returns a list of paths to BGP binary files in a specified directory. BGP files
are identified by the filename format rib.YYMMDD.HHMM.bz2. Paths are returned
as a list of strings.
"""

def get_bgp_binaries_in(directory):
    regex      = compile("rib.\d+.\d+.bz2")
    bgp_files  = []
    dir_walker = walk(directory)
    
    for dir_data in dir_walker:
        path_to_dir = dir_data[0]
        filenames   = dir_data[2]
        
        bgp_files += __filter_valid_files(path_to_dir, filenames, regex)
                
    return bgp_files
    
def __filter_valid_files(path_to_dir, filenames, regex):
    matching_files = []
    
    for filename in filenames:
        if regex.match(filename) is not None
            matching_files.append(path_to_dir + "/" + filename)
            
    return matching_files