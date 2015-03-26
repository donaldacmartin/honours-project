#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from base import BaseAtlas, GLOBAL
from visualisation.base import LIGHT_GREY, LIGHT_GREEN, DARK_RED

class ChronologicalAtlas(BaseAtlas):
    def __init__(self, width, height, old_bgp, new_bgp, region=GLOBAL):
        """
        The aim of this atlas is to show the difference in connections available between
        two BGP dumps (ideally from different time periods). Connections that have
        persisted between the two dumps are shown in grey, connections that are no
        longer available are in red, and new connections are in green.
        """
        super(ChronologicalAtlas, self).__init__(width, height, region)

        self.resolve_bgp_to_asys_coords(old_bgp)
        self.resolve_bgp_to_asys_coords(new_bgp)

        old_cxns = old_bgp.asys_connections
        new_cxns = new_bgp.asys_connections

        unchanged = old_cxns.intersection(new_cxns)
        removed   = old_cxns.difference(new_cxns)
        added     = new_cxns.difference(old_cxns)

        self.draw_international_boundaries()

        self.draw_connections(unchanged, LIGHT_GREY)
        self.draw_connections(removed, DARK_RED)
        self.draw_connections(added, LIGHT_GREEN)
