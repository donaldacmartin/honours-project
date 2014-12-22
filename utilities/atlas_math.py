#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

"""
Atlas Math

Some functions to convert latitude and longitude coordinates into x and y
coordinates on an image.
"""

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