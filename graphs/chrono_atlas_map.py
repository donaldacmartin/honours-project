#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from utilities.geoip import GeoIPLookup
from utilities.atlas_math import map_lat_to_y_coord, map_lon_to_x_coord

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
    def __init__(self, width, height, cxns1, cxns2, ips1, ip2):
        self.added_cxns     = cxns2.difference(cxns1)
        self.removed_cxns   = cxns1.difference(cxns2)
        self.unchanged_cxns = cxns1.intersection(cxns2)
        
        self.asys_coordinates = {}
        
        self.geoip = GeoIPLookup()
        self.image = new("RGB", (width, height), "white")
        
        for (asys, ip_address) in dict(ips1.items() + ips.items()).items():
            self.__map_as_ip_to_coordinates(asys, ip_address)

        self.__draw()
        
    def __map_as_ip_to_coordinates(self, as_num, ip_address):
        try:
            lat,lon       = self.geoip.get_latlon_for_ip(ip_address)
            width, height = self.image.size
            
            x = map_lon_to_x_coord(lon, width)
            y = map_lat_to_y_coord(lat, height)
            
            self.asys_coordinates[as_num] = (x,y)
        except NameError as e:
            logging.warning("No LatLon for" + str(as_num))
        
    def __draw(self):
        draw_cursor = Draw(self.image)
        
        for (start, end) in self.unchanged_cxns:
            self.__draw_link(start, end, draw_cursor, (162,162,162))
            
        for (start, end) in self.removed_cxns:
            self.__draw_link(start, end, draw_cursor, (255, 59, 59))
        
        for (start, end) in self.added_cxns:
            self.__draw_link(start, end, draw_cursor, (59, 255, 134))
    
    def __draw_link(self, start, end, draw, colour):
        try:
            start_xy = self.asys_coordinates[start]
            end_xy   = self.asys_coordinates[end]
            draw.line([start_xy, end_xy], fill=colour, width=1)
        except KeyError as e:
            logging.warning("AtlasMap: AS" + str(e) + " not in list of coords")
            
    def save(self, filename, filetype="PNG"):
        self.image.save(filename, filetype)