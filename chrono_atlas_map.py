#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from atlas_map import map_lon_to_x_coord, map_lat_to_y_coord
from geoip import GeoIPLookup
from Image import new
from ImageDraw import Draw
import logging

class ChronologicalAtlasMap(object):
    def __init__(self, filename, width, height):
        self.connections_added     = set()
        self.connections_removed   = set()
        self.connections_unchanged = set()
        self.asys_coordinates      = {}
        
        self.geoip    = GeoIPLookup()
        
        self.filename = filename
        self.image    = new("RGB", (width, height), "white")
        
    def add_auto_sys_ip(self, as_num, ip_address):
        if int(as_num) in self.asys_coordinates:
            return
            
        try:
            lat,lon       = self.geoip.get_latlon_for_ip(ip_address)
            as_num        = int(as_num)
            width, height = self.image.size
            
            x = map_lon_to_x_coord(lon, width)
            y = map_lat_to_y_coord(lat, height)
            
            self.asys_coordinates[as_num] = (x,y)
        except:
            logging.warning("AtlasMap: unable to add " + str(as_num))
            
    def __get_connection(self, start, end):
        start = int(start)
        end   = int(end)
        return (min(start,end), max(start,end))
        
    def add_new_link(self, start, end):
        self.connections_added.add(self.__get_connection(start, end))
    
    def add_removed_link(self, start, end):
        self.connections_removed.add(self.__get_connection(start, end))
        
    def add_unchanged_link(self, start, end):
        self.connections_unchanged.add(self.__get_connection(start, end))
        
    def draw_graph(self):
        draw_cursor = Draw(self.image)
        
        for (start, end) in self.connections_unchanged:
            self.__draw_link(start, end, draw_cursor, (212,212,212))
                
        for (start, end) in self.connections_removed:
            self.__draw_link(start, end, draw_cursor, (128,0,0))
                
        for (start, end) in self.connections_added:
            self.__draw_link(start, end, draw_cursor, (55,237,91))
            
        self.image.save(self.filename, "PNG")
    
    def __draw_link(self, start, end, draw, colour_value):
        try:
            start_xy = self.asys_coordinates[start]
            end_xy   = self.asys_coordinates[end]
            draw.line([start_xy, end_xy], fill=colour_value, width=1)
        except KeyError as e:
            logging.warning("AtlasMap: AS" + str(e) + " not in list of coords")