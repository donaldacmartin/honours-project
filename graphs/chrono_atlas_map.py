#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from atlas_map import AtlasMap
from graph import LIGHT_GREY, LIGHT_GREEN, DARK_RED

"""
AtlasMap

Generates a connected graph of autonomous systems based on their geographical
locations. Takes the following parameters:
- width                 image width in pixels
- hash                  image height in pixels
- asys_connections      set of connections between ASs as integers (as1, as2)
- asys_ip_addresses     dictionary mapping integer AS to string IP address
"""

class ChronoAtlasMap(AtlasMap):
    def __init__(self, width, height, old_bgp, new_bgp):
        super(ChronoAtlasMap, self).__init__(width, height, old_bgp, LIGHT_GREY)
        
        for (asys, ip_address) in new_bgp.as_to_ip_address.items():
            super(ChronoAtlasMap, self).__map_as_ip_to_coordinates(asys, ip_address)
        
        old_cxns = old_bgp.as_connections
        new_cxns = new_bgp.as_connections
        
        new_connections     = new_cxns.difference(old_cxns)
        removed_connections = old_cxns.difference(new_cxns)

        for (start, end) in removed_connections:
            super(ChronoAtlasMap, self).__draw_line(start, end, DARK_RED)
            
        for (start, end) in new_connections:
            super(ChronoAtlasMap, self).__draw_line(start, end, LIGHT_GREEN)