#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from math import sin, cos, radians, sqrt
from base import BaseGraph, DARK_RED
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
    def __init__(self, width, height, bgp_dump):
        super(RingGraph, self).__init__(width, height)
        self.geoip = GeoIPLookup()
        self.asys_coords = {}

        for (asys, ip_addresses) in bgp_dump.asys_to_ip_addr.items():
            self.map_as_ip_to_circumference_pos(asys, ip_addresses)

        for (start, end) in bgp_dump.asys_connections:
            self.draw_connection(start, end)

    def map_as_ip_to_circumference_pos(self, as_num, ip_addresses):
        lon = self.get_longitude_for_ip_addrs(ip_addresses)

        if lon is None:
            return

        lon           = radians(lon)
        width, height = self.image.size
        centre_x      = width / 2
        centre_y      = height / 2

        x = centre_x + (centre_x * cos(lon))
        y = centre_y + (centre_y * sin(lon))

        self.asys_coords[as_num] = (x,y)

    def get_longitude_for_ip_addrs(self, ip_addresses):
        while len(ip_addresses) > 0:
            try:
                ip_address = ip_addresses.pop()
                return self.geoip.get_latlon_for_ip(ip_address)[1] + 180
            except:
                continue

        return None

    def draw_connection(self, start, end):
        if start not in self.asys_coords or end not in self.asys_coords:
            return

        start = self.asys_coords[start]
        end   = self.asys_coords[end]

        self.draw_line(start, end, DARK_RED)
