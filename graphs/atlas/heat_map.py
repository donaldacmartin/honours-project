#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from graphs.graph import Graph

"""
HeatMap

An object that converts a BGP dump into an atlas map, where each country is
shaded according to the number of IPv4 addresses per capita.

Goals
 - Break BGP data into countries
 - Load population data for each country
 - Load shapefiles
 - Draw and shade
"""

class HeatMap(Graph):
    def __init__(self, bgp_dump, region=GLOBAL, width=1920, height=1080):
        super(HeatMap, self).__init__(width, height)

    
