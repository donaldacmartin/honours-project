#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from math import sin, cos
from graphs.graph import Graph
from utilities.geoip import GeoIPLookup

"""
RingGraph

Generates a connected graph of autonomous systems, stored in a ring. Each AS is
stored at a set radius.

LayeredRingGraph

A subclass of RingGraph that also generates a connected graph of autonomous
systems in a series of rings, based on the number of connections that each AS
has to other ASs.
"""

class RingGraph(Graph):
    def __init__(self, width, bgp_dump):
        super(RingGraph, self).__init__(width, width)
        self.geoip = GeoIPLookup()

        self.asys_coords = {}
        self.fast_reject = set()

        for (asys, ip_address) in bgp_dump.as_to_ip_address.items():
            self._map_as_ip_to_circumference_pos(asys, ip_address)

        for (start, end) in bgp_dump.as_connections:
            self._draw_connection(start, end)

    def _map_as_ip_to_circumference_pos(self, as_num, ip_addr):
        try:
            if as_num in self.asys_coords or as_num in self.fast_reject:
                return

            lat,lon = self.geoip.get_latlon_for_ip(ip_address)
            width, height = self.image.size

            radius = (width - 10) / 2
            centre = (width / 2, height / 2)

            x = centre[0] + (radius * sin(lon))
            y = centre[1] - (radius * cos(lon))

            self.asys_coords[as_num] = (x,y)
        except:
            self.fast_reject.add(as_num)

    def _draw_connection(self, start, end):
        if coord_missing(start, end, self.asys_coords):
            return

        start = self.asys_coords[start]
        end   = self.asys_coords[end]

        super(RingGraph, self).draw_line(start, end)

def coord_missing(start, end, coords):
    return not all(asys in coords for asys in [start,end])
