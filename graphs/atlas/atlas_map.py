#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from utilities.geoip import GeoIPLookup
from graphs.graph import Graph, DARK_RED
from utilities.shapefile import Reader
from ImageDraw import Draw

"""
AtlasMap

Generates a connected graph of autonomous systems based on their geographical
locations. Takes the following parameters:
- width                 image width in pixels
- hash                  image height in pixels
- asys_connections      set of connections between ASs as integers (as1, as2)
- asys_ip_addresses     dictionary mapping integer AS to string IP address
"""

AFRICA        = ((36.08, -21.62), (-38.50, 50.45))
# ASIA          = () - This is too big to make a difference
EUROPE        = ((61.16, -11.51), (35.63, 33.66))
NORTH_AMERICA = ((62.95, -167.52), (17.04, -52.56))
SOUTH_AMERICA = ((10.21, -92.64), (-54.94, -35.33))

class AtlasMap(Graph):
    def __init__(self, width, height, bgp, latlon_limits=None, line_colour=DARK_RED):
        super(AtlasMap, self).__init__(width, height)
        
        self.geoip = GeoIPLookup()
        self.asys_coords = {}
        self.fast_reject = set()
        scaled           = False
        
        for (asys, ip_address) in bgp.as_to_ip_address.items():
            self._map_as_ip_to_coordinates(asys, ip_address)
            
        if latlon_limits is not None:
            self._scale_coords(latlon_limits)
            draw_borders(self.image, latlon_limits)
            scaled = True

        for (start, end) in bgp.as_connections:
            self._draw_line(start, end, line_colour, scaled)
        
    def _map_as_ip_to_coordinates(self, as_num, ip_address):
        try:
            if as_num in self.asys_coords or as_num in self.fast_reject:
                return
                
            lat,lon = self.geoip.get_latlon_for_ip(ip_address)
            width, height = self.image.size
            
            x = map_lon_to_x_coord(lon, width)
            y = map_lat_to_y_coord(lat, height)
            
            self.asys_coords[as_num] = (x,y)
        except:
            self.fast_reject.add(as_num)
            
    def _scale_coords(self, (limit1, limit2)):
        img_width, img_height = self.image.size
        
        x1 = map_lon_to_x_coord(limit1[1], img_width)
        x2 = map_lon_to_x_coord(limit2[1], img_width)
        
        y1 = map_lat_to_y_coord(limit1[0], img_height)
        y2 = map_lat_to_y_coord(limit2[0], img_height)
        
        x_anchor = min(x1, x2)
        y_anchor = min(y1, y2)
        
        x_scale = img_width / abs(x2 - x1)
        y_scale = img_height / abs(y2 - y1)

        for (asys, (x,y)) in self.asys_coords.items():
            new_x = (x - x_anchor) * x_scale
            new_y = (y - y_anchor) * y_scale
            self.asys_coords[asys] = (new_x, new_y)
            
    def _draw_line(self, start, end, colour, scaled):
        if coord_missing(start, end, self.asys_coords):
            return
            
        start = self.asys_coords[start]
        end   = self.asys_coords[end]
        
        if not scaled and should_wrap_over_pacific(start, end, self.image):
            self._draw_transpacific_connection(start, end, colour)
        else:
            self._draw_connection(start, end, colour)
            
    def _draw_connection(self, start, end, colour):
        super(AtlasMap, self).draw_line(start, end, colour)
        
    def _draw_transpacific_connection(self, start, end, colour):
        start_x, start_y      = start
        end_x, end_y          = end
        img_width, img_height = self.image.size
        
        dx = end_x - start_x
        dy = end_y - start_y

        line_1_x = img_width if start_closer_to_RHS(start_x, img_width) else 0    
        line_2_x = img_width - line_1_x
        lines_y  = start_y - (((line_1_x - start_x) / dx) * dy)
        
        super(AtlasMap, self).draw_line(start, (line_1_x, lines_y), colour)
        super(AtlasMap, self).draw_line(end, (line_2_x, lines_y), colour)
            
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
    
def draw_borders(img, (limit1, limit2)=None):
    reader = Reader("utilities/data/country_outlines/countries")
    draw = Draw(img)
    
    x1 = map_lon_to_x_coord(limit1[1], img.size[0])
    x2 = map_lon_to_x_coord(limit2[1], img.size[0])

    y1 = map_lat_to_y_coord(limit1[0], img.size[1])
    y2 = map_lat_to_y_coord(limit2[0], img.size[1])

    x_anchor = min(x1, x2)
    y_anchor = min(y1, y2)

    x_scale = img.size[0] / abs(x2 - x1)
    y_scale = img.size[1] / abs(y2 - y1)

    for record in reader.shapeRecords():
        points  = record.shape.points
        outline = []
        
        for (lon, lat) in points:
            x = (map_lon_to_x_coord(lon, img.size[0]) - x_anchor) * x_scale
            y = (map_lat_to_y_coord(lat, img.size[1]) - y_anchor) * y_scale
            outline.append((x,y))
        
        for i in range(1, len(outline)):
            draw.line([outline[i-1], outline[i]], fill="black", width=3)
        #draw.polygon(outline, outline="black")