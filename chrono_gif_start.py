#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from threading import Thread
from chrono_atlas_map import MonthlyTimeline
from file import *


all_files = get_bgp_files_under_directory("/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/")
files_to_use = []
bgp_dumps = {}

for year in range(2001, 2015):
    date = "rib." + str(year) + "10"

    for bgp_file in all_files:
        if date in bgp_file:
            files_to_use.append(bgp_file)
            break
           
    if len(files_to_use) >= 3:
        break
                
MonthlyTimeline(files_to_use)