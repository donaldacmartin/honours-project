#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from graphs.atlas.atlas_map import AtlasMap
from graphs.graph import LIGHT_GREY, LIGHT_GREEN, DARK_RED

"""
ChronoAtlasMap
"""

class ChronoAtlasMap(AtlasMap):
    def __init__(self, width, height, old_bgp, new_bgp):
        super(ChronoAtlasMap, self).__init__(width, height, old_bgp, LIGHT_GREY)
        
        for (asys, ip_addr) in new_bgp.as_to_ip_address.items():
            super(ChronoAtlasMap, self)._map_as_ip_to_coordinates(asys, ip_addr)
        
        removed_cxns = old_bgp.as_connections.difference(new_bgp.as_connections)
        new_cxns     = new_bgp.as_connections.difference(old_bgp.as_connections)
        
        self.__setup_and_draw(removed_cxns, DARK_RED)
        self.__setup_and_draw(new_cxns, LIGHT_GREEN)

    def __setup_and_draw(self, connections, colour):
        for (start, end) in connections:
            super(ChronoAtlasMap, self)._draw_line(start, end, colour)