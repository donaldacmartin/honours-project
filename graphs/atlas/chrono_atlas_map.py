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

class ChronologicalAtlas(BaseAtlas):
    def __init__(self, width, height, old_bgp, new_bgp, region=GLOBAL):
        super(ChronologicalAtlas, self).__init__(width, height, region)

        self.resolve_bgp_to_asys_coords(old_bgp)
        self.resolve_bgp_to_asys_coords(new_bgp)

        old_cxns = old_bgp.asys_connections

        removed_cxns = old_bgp.asys_connections.difference(new_bgp.asys_connections)
        new_cxns     = new_bgp.asys_connections.difference(old_bgp.asys_connections)

        self._setup_and_draw(removed_cxns, DARK_RED)
        self._setup_and_draw(new_cxns, LIGHT_GREEN)

    def _setup_and_draw(self, connections, colour):
        for (start, end) in connections:
            super(ChronoAtlasMap, self)._draw_line(start, end, colour)
