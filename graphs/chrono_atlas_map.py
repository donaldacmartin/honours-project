#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from atlas_map import AtlasMap

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
    def __init__(self, width, height, cxns1, cxns2, ips1, ips2):
        ip_addrs = dict(ips1.items() + ips2.items())
        conns    = cxns1.intersection(cxns2)
        
        super(ChronoAtlasMap, self).__init__(width, height, conns, ip_addrs, (162,162,162))
        
        new_connections     = cxns2.difference(cxns1)
        removed_connections = cxns1.difference(cxns2)

        for (start, end) in removed_connections:
            super(ChronoAtlasMap, self).__draw_line(start, end, (255, 59, 59))
            
        for (start, end) in new_connections:
            super(ChronoAtlasMap, self).__draw_line(start, end, (59, 255, 134))