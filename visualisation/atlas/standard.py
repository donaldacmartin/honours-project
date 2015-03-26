#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from base import BaseAtlas, GLOBAL

class StandardAtlas(BaseAtlas):
    """
    This is the most basic form of atlas that can be produced from a BGP dump. The
    data is simply placed onto the map, and connections are drawn between the
    approximate locations of the autonomous systems.
    """
    
    def __init__(self, bgp_dump, width=1920, height=1080, region=GLOBAL):
        super(StandardAtlas, self).__init__(width, height, region)

        self.resolve_bgp_to_asys_coords(bgp_dump)
        self.draw_international_boundaries()
        self.draw_connections(bgp_dump.asys_connections)
