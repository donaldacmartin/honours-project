#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from utilities.shapefile import Reader
from graphs.atlas.atlas_map import map_lon_to_x_coord, map_lat_to_y_coord
from ImageDraw import Draw

def draw_borders(img, (limit1, limit2)=None):
    reader = Reader("utilities/data/country_outlines/countries")
    draw = Draw(img)

    x1 = map_lon_to_x_coord(limit1[1], img.size[0])
    x2 = map_lon_to_x_coord(limit2[1], img.size[0])

    y1 = map_lat_to_y_coord(limit1[0], img.size[1])
    y2 = map_lat_to_y_coord(limit2[0], img.size[1])

    x_anchor = min(x1, x2)
    y_anchor = min(y1, y2)

    x_scale = img_width / abs(x2 - x1)
    y_scale = img_height / abs(y2 - y1)

    for record in reader.shapeRecords():
        points  = record.shape.points
        outline = []

        for (lon, lat) in points:
            x = (map_lon_to_x_coord(lon, img.size[0]) - x_anchor) * x_scale
            y = (map_lat_to_y_coord(lat, img.size[1]) - y_anchor) * y_scale

        draw.polygon(outline, outline="black")

def load_countries():
    reader = Reader("utilities/data/country_outlines/countries")
    
