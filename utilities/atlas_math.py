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
    centre = (img_height - 10) / 2.0
    delta  = (img_height - 10) / 180.0
    return centre - (lat_coord * delta)
    
def map_lon_to_x_coord(lon_coord, img_width):
    centre = (img_width - 10) / 2.0
    delta  = (img_width - 10) / 360.0
    return centre + (lon_coord * delta)