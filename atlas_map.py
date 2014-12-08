#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from geoip import GeoIPLookup
from Image import new
from ImageDraw import Draw
import logging

"""
AtlasMap

Generates a connected graph of autonomous systems based on their geographical
locations. Connections between autonomous systems are stored in a set to save
space and to avoid doubly drawing lines. GeoIP is a module that converts AS
numbers into latlon coordinates. If a link contains an AS number that does not
map to valid coordinates, the link is discarded and a warning message logged.
"""

class AtlasMap(object):
    def __init__(self, filename, width, height):
        self.asys_connections = set()
        self.coords_for_asys  = {}
        
        self.geoip    = GeoIPLookup()
        
        self.filename = filename
        self.image    = Image.new("RGB", (width, height), "white")
        
    def add_auto_sys_ip(self, as_num, ip_addr):
        lat,lon = self.geoip.get_latlon_for_ip(ip_addr)
        as_num  = int(as_num)
        
        x = map_lon_to_x_coord(lon, self.image.size[0])
        y = map_lat_to_y_coord(lat, self.image.size[1])
        
        self.coords_for_asys[as_num] = (x,y)
        
    def add_link(self, start, end):
        start = int(start)
        end   = int(end)
        
        connection = (min(start,end), max(start,end))
        self.asys_connections.add(connection)
        
    def draw_graph(self):
        draw = ImageDraw.Draw(self.image)

        for (start, end) in self.links:
            self.__draw_link(start, end, draw)
            
        self.image.save(self.filename, "PNG")
    
    def __draw_link(self, start, end, draw):
        try:
            start_xy = self.coords_for_asys[start]
            end_xy   = self.coords_for_asys[end]
            draw.line([start_xy, end_xy], fill=128, width=1)
        except KeyError as e:
            logging.warning("Atlas Mapper encountered a non-fatal error")
            logging.warning("AS" + str(e) + " not in list of coordinates")
            
def map_lat_to_y_coord(lat_coord, img_height):
    centre = (img_height - 10) / 2.0
    delta  = (img_height - 10) / 180.0
    
    return centre - (lat__cord * delta)
    
def map_lon_to_x_coord(lon_coord, img_width):
    centre = (img_width - 10) / 2.0
    delta  = (img_width - 10) / 360.0
    
    return centre + (lon_coord * delta)