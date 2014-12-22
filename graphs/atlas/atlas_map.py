#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from utilities.geoip import GeoIPLookup
from graphs.graph import Graph, DARK_RED

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
    def __init__(self, width, height, bgp_dump, line_colour=DARK_RED):
        super(AtlasMap, self).__init__(width, height)
        
        self.geoip = GeoIPLookup()
        self.asys_coords = {}
        self.fast_reject = set()
        
        for (asys, ip_address) in bgp_dump.as_to_ip_address.items():
            self.__map_as_ip_to_coordinates(asys, ip_address)

        for (start, end) in bgp_dump.as_connections:
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
            
    def __draw_connection(self, start, end, colour):
        super(AtlasMap, self).draw_line(start, end, colour)
        
    def __draw_transpacific_connection(self, start, end, colour)
        start_x, start_y      = start
        end_x, end_y          = end
        img_width, img_height = image.size
        draw_cursor           = Draw(image)

        dx = end_x - start_x
        dy = end_y - start_y

        line_1_x = img_width if start_closer_to_RHS(start_x, img_width) else 0    
        line_2_x = img_width - line_1_x
        lines_y  = start_y - (((line_1_x - start_x) / dx) * dy)
        
        super(AtlasMap, self).draw_line(start, (line_1_x, lines_y), colour)
        super(AtlasMap, self).draw_line(end, (line_1_x, lines_y), colour)
            
# ------------------------------------------------------------------------------
# Helper Maths Functions
# ------------------------------------------------------------------------------
def map_lat_to_y_coord(lat_coord, img_height):
    img_centre     = (img_height - 10) / 2.0
    pixels_per_deg = (img_height - 10) / 180.0
    return img_centre - (lat_coord * pixels_per_deg)
    
def map_lon_to_x_coord(lon_coord, img_width):
    img_centre     = (img_width - 10) / 2.0
    pixels_per_deg = (img_width - 10) / 360.0
    return img_centre + (lon_coord * pixels_per_deg)
    
def should_wrap_over_pacific(start, end, image):
    start_x   = start[0]
    end_x     = end[0]
    img_width = image.size[0]
    
    return abs(end_x - start_x) > (img_width / 2)
    
def coord_missing(start, end, coords):
    return not all(asys in coords for asys in [start,end])
        
def start_closer_to_RHS(start_x, img_width):
    return (img_width - start_x) < start_x