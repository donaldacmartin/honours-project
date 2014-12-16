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
    def __init__(self, width, height, cxns1, cxns2, ips1, ips2, asys_coords):
        self.ip_addresses   = dict(ips1.items() + ips2.items())
        
        self.added_cxns     = cxns2.difference(cxns1)
        self.removed_cxns   = cxns1.difference(cxns2)
        self.unchanged_cxns = cxns1.intersection(cxns2)
        
        self.asys_coordinates = asys_coords
        self.fail_counter   = 0
        
        self.geoip = GeoIPLookup()
        self.image = new("RGB", (width, height), "white")

        self.__draw()
        
    def __get_coords(self, asys):
        if asys in self.asys_coordinates:
            return self.asys_coordinates[asys]
        
        return self.__map_as_ip_to_coordinates(asys)
        
    def __map_as_ip_to_coordinates(self, as_num):
        try:
            if as_num not in self.ip_addresses:
                raise NameError("ASYS does not map to IP address")
                
            ip_address    = self.ip_addresses[as_num]
            lat,lon       = self.geoip.get_latlon_for_ip(ip_address)
            width, height = self.image.size
            
            x = map_lon_to_x_coord(lon, width)
            y = map_lat_to_y_coord(lat, height)
            
            self.asys_coordinates[as_num] = (x,y)
            return (x,y)
        except NameError as e:
            logging.warning("No LatLon for " + str(as_num))
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
        
        print("Unable to draw " + str(self.fail_counter) + " of " + str(total))
        print("Failure rate: " + str((fail_counter / total) * 100) + "%")
    
    def __draw_link(self, start, end, draw, colour):
        try:
            start_xy = self.__get_coords(start)
            end_xy   = self.__get_coords(end)
            
            if abs(end_xy[0] - start_xy[0]) > (self.image.size[0] / 2):
                mid_y = abs((start_xy[1] + end_xy[1]) / 2)
                
                if (self.image.size[0] - start[0] < start[0]):
                    x1 = self.image.size[0]
                else:
                    x1 = 0
                    
                x2 = self.image.size[0] - x1
                
                draw.line([start_xy, (x1, mid_y)], fill=colour, width=1)
                draw.line([(x2, mid_y), end_xy], fill=colour, width=1)
                
            draw.line([start_xy, end_xy], fill=colour, width=1)
        except:
            self.fail_counter += 1
            
    def save(self, filename, filetype="PNG"):
        self.image.save(filename, filetype)