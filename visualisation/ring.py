#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from math import sin, cos
from graphs.base import BaseGraph, DARK_RED
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

class RingGraph(BaseGraph):
    def __init__(self, width, bgp_dump):
        super(RingGraph, self).__init__(width, width)
        self.geoip = GeoIPLookup()
        self.asys_coords = {}
        self.fast_reject = set()

        for (asys, ip_addresses) in bgp_dump.asys_ip_address.items():
            self.map_as_ip_to_circumference_pos(asys, ip_addresses)

        for (start, end) in bgp_dump.asys_connections:
            self.draw_connection(start, end)

    def map_as_ip_to_circumference_pos(self, as_num, ip_addresses):
        while (len(ip_addresses) > 0 and lon != None):
            try:
                ip_address = ip_addresses.pop()
                lon        = self.geoip.get_latlon_for_ip(ip_address)[1] + 180
            except:
                lon = None

        if lon is None:
            return

        width  = self.image.size[0]
        radius = (width - 10) / 2
        centre = width / 2

        x = centre + radius * cos(lon)
        y = centre + radius * sin(lon)

        self.asys_coords[as_num] = (x,y)

    def draw_connection(self, start, end):
        if start not in self.asys_coords or end not in self.asys_coords:
            return

        start = self.asys_coords[start]
        end   = self.asys_coords[end]

        self.draw_line(start, end, DARK_RED)
