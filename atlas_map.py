#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from geoip import GeoIPLookup
import Image, ImageDraw

class AtlasMap(object):
    def __init__(self, filename, width, height):
        self.links = []
        self.plot_positions = {}
        self.filename = filename
        
        self.geoip  = GeoIPLookup("data/locations.csv", "data/blocks.csv")
        
        self.width  = width
        self.height = height
        self.image  = Image.new("RGB", (width, height), "white")
        
    def add_auto_sys_ip(self, as_num, ip_addr):
        lat,lon = self.geoip.get_latlon_for_ip(ip_addr)
        as_num  = int(as_num)
        
        x = __map_lon_to_x_coord(lon)
        y = __map_lat_to_y_coord(lat)
        
        self.plot_positions[as_num] = (x,y)
        
    def add_link(self, start, end):
        start = int(start)
        end   = int(end)
        
        self.links.append((start,end))
        
    def draw_graph(self):
        draw   = ImageDraw.Draw(self.image)
        centre = ((self.width - 10) / 2, (self.height - 10) / 2)
        
        for (start, end) in self.links:
            start_x, start_y = self.plot_positions[start]
            end_x, end_y     = self.plot_positions[end]
            
            draw.line((start_x, start_y, end_x, end_y), fill=128, width=1)
            
        self.image.save(self.filename, "PNG")
            
    def __map_lat_to_y_coord(lat):
        centre = (self.height - 10) / 2
        delta  = (self.height - 10) / 180.0
        
        return centre - (lat * delta)
        
    def __map_lon_to_x_coord(lon):
        centre = (self.width - 10) / 2
        delta  = (self.width - 10) / 360.0
        
        return centre + (lon * delta)