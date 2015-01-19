#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from graphs.atlas.atlas_map import AtlasMap, GLOBAL
from graphs.graph import LIGHT_GREY, LIGHT_GREEN, DARK_RED

"""
ChronoAtlasMap
"""

class ChronoAtlasMap(AtlasMap):
    def __init__(self, width, height, old_bgp, new_bgp, region=GLOBAL):
        super(ChronoAtlasMap, self).__init__(width, height, old_bgp, region, LIGHT_GREY)

        for (asys, ip_addresses) in new_bgp.asys_ip_address.items():
            self._map_as_ip_to_coordinates(asys, ip_addresses)

        removed_cxns = old_bgp.asys_connections.difference(new_bgp.asys_connections)
        new_cxns     = new_bgp.asys_connections.difference(old_bgp.asys_connections)

        self._setup_and_draw(removed_cxns, DARK_RED)
        self._setup_and_draw(new_cxns, LIGHT_GREEN)

    def _setup_and_draw(self, connections, colour):
        for (start, end) in connections:
            super(ChronoAtlasMap, self)._draw_line(start, end, colour)
