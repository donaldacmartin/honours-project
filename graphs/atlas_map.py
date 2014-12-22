#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from utilities.geoip import GeoIPLookup
from utilities.atlas_math import map_lat_to_y_coord, map_lon_to_x_coord
from utilities.atlas_math import should_wrap_over_pacific
from utilities.atlas_math import coord_missing

from utilities.atlas_imaging import draw_connection
from utilities.atlas_imaging import draw_transpacific_connection

from graph import Graph

"""
AtlasMap

Generates a connected graph of autonomous systems based on their geographical
locations. Takes the following parameters:
- width                 image width in pixels
- hash                  image height in pixels
- asys_connections      set of connections between ASs as integers (as1, as2)
- asys_ip_addresses     dictionary mapping integer AS to string IP address
"""

class AtlasMap(Graph):
    def __init__(self, width, height, asys_conns, asys_ip_addrs, line_colour=128):
        super(AtlasMap, self).__init__()
        
        self.geoip = GeoIPLookup()
        self.asys_coords = {}
        self.fast_reject = set()
        
        for (asys, ip_address) in asys_ip_addrs.items():
            self.__map_as_ip_to_coordinates(asys, ip_address)

        for (start, end) in asys_conns:
            self.__draw_line(start, end, line_colour)
        
    def __map_as_ip_to_coordinates(self, as_num, ip_address):
        try:
            if as_num in self.asys_coordinates or as_num in self.fast_reject:
                return
                
            lat,lon = self.geoip.get_latlon_for_ip(ip_address)
            width, height = self.image.size
            
            x = map_lon_to_x_coord(lon, width)
            y = map_lat_to_y_coord(lat, height)
            
            self.asys_coordinates[as_num] = (x,y)
        except:
            self.fast_reject.add(as_num)
            
    def __draw_line(self, start, end, colour):
        if coord_missing(start, end, self.asys_coords):
            return
            
        start = self.asys_coords[start]
        end   = self.asys_coords[end]
        
        if should_wrap_over_pacific(start, end, self.image):
            draw_transpacific_connection(start, end, self.image, colour)
        else:
            draw_connection(start, end, self.image, colour)