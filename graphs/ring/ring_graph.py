#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from math import sin, cos
from graphs.graph import Graph

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
        
        self.asys_coordinates = {}
        self.fast_reject      = set()
        
        for (asys, ip_address) in bgp_dump.as_to_ip_address.items():
            self.__map_as_ip_to_circumference_pos(asys, ip_address)
        
        for (start, end) in bgp_dump.as_connections:
            self.__draw_connection(start, end)
        
    def __map_as_ip_to_circumference_pos(self, asys, ip_addr):
        try:
            if as_num in self.asys_coordinates or as_num in self.fast_reject:
                return
                
            lat,lon = self.geoip.get_latlon_for_ip(ip_address)
            width, height = self.image.size
            
            radius = (width - 10) / 2
            centre = (width / 2, height / 2)
            
            x = centre[0] + (radius * sin(lon))
            y = centre[1] - (radius * cos(lon))

            self.asys_coordinates[as_num] = (x,y)
        except:
            self.fast_reject.add(as_num)
            
    def __draw_connection(self, start, end):
        if coord_missing(start, end, self.asys_coords):
            return
            
        start = self.asys_coords[start]
        end   = self.asys_coords[end]

        super(RingGraph, self).draw_line(start, end)

def coord_missing(start, end, coords):
    return not all(asys in coords for asys in [start,end])
    
"""
class LayeredRingGraph(RingGraph):
    def __calculate_asys_coordinates(self):
        angle_delta   = 360.0 / len(self.asys_connections)
        width, height = self.image.size
        
        centre = (width / 2, height / 2)
        
        most_cxns   = max([len(cxns) for cxns in self.asys_connections.values()])
        std_radius  = (width - 10) / 2
        radius_step = std_radius / most_cxns
        
        angle = 0
        
        for (asys, connections) in self.asys_connections.items():
            radius = std_radius - (len(connections) * radius_step)
            x = centre[0] - (radius * sin(angle))
            y = centre[1] - (radius * cos(angle))
            
            self.asys_coordinates[asys] = (x,y)
            angle += angle_delta
        
        super(LayeredRingGraph, self).draw()
"""