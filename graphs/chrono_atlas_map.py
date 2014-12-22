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

from Image import new
from ImageDraw import Draw

import logging

"""
AtlasMap

Generates a connected graph of autonomous systems based on their geographical
locations. Takes the following parameters:
- width                 image width in pixels
- hash                  image height in pixels
- asys_connections      set of connections between ASs as integers (as1, as2)
- asys_ip_addresses     dictionary mapping integer AS to string IP address
"""

class ChronologicalAtlasMap(object):
    def __init__(self, width, height, cxns1, cxns2, ips1, ips2, asys_coords):
        self.ip_addresses   = dict(ips1.items() + ips2.items())
        
        self.added_cxns     = cxns2.difference(cxns1)
        self.removed_cxns   = cxns1.difference(cxns2)
        self.unchanged_cxns = cxns1.intersection(cxns2)
        
        self.asys_coordinates = asys_coords
        self.fast_reject      = set()
        
        self.geoip = GeoIPLookup()
        self.image = new("RGB", (width, height), "white")

        self.__draw()
        
    def __get_coords(self, asys):
        if asys in self.asys_coordinates:
            return self.asys_coordinates[asys]
        
        return self.__map_as_ip_to_coordinates(asys)
        
    def __map_as_ip_to_coordinates(self, as_num):
        try:
            if as_num in self.fast_reject:
                raise NameError("Nope")
                
            if as_num not in self.ip_addresses:
                self.fast_reject.add(as_num)
                raise NameError("ASYS does not map to IP address")
                
            ip_address    = self.ip_addresses[as_num]
            lat,lon       = self.geoip.get_latlon_for_ip(ip_address)
            width, height = self.image.size
            
            x = map_lon_to_x_coord(lon, width)
            y = map_lat_to_y_coord(lat, height)
            
            self.asys_coordinates[as_num] = (x,y)
            return (x,y)
        except NameError as e:
            self.fast_reject.add(as_num)
            raise
        
    def __draw(self):
        draw_cursor = Draw(self.image)
        
        for (start, end) in self.unchanged_cxns:
            self.__draw_link(start, end, draw_cursor, (162,162,162))
            
        for (start, end) in self.removed_cxns:
            self.__draw_link(start, end, draw_cursor, (255, 59, 59))
        
        for (start, end) in self.added_cxns:
            self.__draw_link(start, end, draw_cursor, (59, 255, 134))
        
        total = len(self.unchanged_cxns) + len(self.removed_cxns) + len(self.added_cxns)
    
    def __draw_link(self, start, end, draw, colour):
        try:
            start = self.__get_coords(start)
            end   = self.__get_coords(end)
            
            if should_wrap_over_pacific(start, end, self.image):
                draw_transpacific_connection(start, end, self.image, colour)
            else:
                draw_connection(start, end, self.image, colour)
        except:
            pass
            
    def save(self, filename, filetype="PNG"):
        self.image.save(filename, filetype)