#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from utilities.geoip import GeoIPLookup
from graphs.graph import BaseGraph, DARK_RED
from utilities.shapefile import Reader
from ImageDraw import Draw

GLOBAL        = ((90, 180), (-90,-180))
AFRICA        = ((36.08, -21.62), (-38.50, 50.45))
EUROPE        = ((61.16, -11.51), (35.63, 33.66))
NORTH_AMERICA = ((62.95, -167.52), (17.04, -52.56))
SOUTH_AMERICA = ((10.21, -92.64), (-54.94, -35.33))

class AtlasMap(BaseGraph):
    def __init__(self, width, height, bgp, region=GLOBAL, line_colour=DARK_RED):
        super(AtlasMap, self).__init__(width, height)

        self.geoip       = GeoIPLookup()
        self.asys_coords = {}
        self.fast_reject = set()
        self.region      = region

        self._draw_borders()

        for (asys, ip_addresses) in bgp.asys_ip_address.items():
            self._map_as_ip_to_coordinates(asys, ip_addresses)

        for (start, end) in bgp.asys_connections:
            self._draw_line(start, end, line_colour)

    def _map_as_ip_to_coordinates(self, as_num, ip_addresses):
        try:
            if len(ip_addresses) == 0:
                self.fast_reject.add(as_num)
                return

            if as_num in self.asys_coords or as_num in self.fast_reject:
                return

            ip_address = ip_addresses.pop()
            latlon     = self.geoip.get_latlon_for_ip(ip_address)
            xy_coord   = scale_coords(latlon, self.region, self.image)
            self.asys_coords[as_num] = xy_coord
        except:
            try:
                self._map_as_ip_to_coordinates(as_num, ip_addresses)
            except:
                self.fast_reject.add(as_num)

    def _draw_line(self, start, end, colour):
        if coord_missing(start, end, self.asys_coords):
            return

        start = self.asys_coords[start]
        end   = self.asys_coords[end]

        if self.region == GLOBAL and should_wrap_over_pacific(start, end, self.image):
            self._draw_transpacific_connection(start, end, colour)
        else:
            self._draw_connection(start, end, colour)

    def _draw_connection(self, start, end, colour):
        super(AtlasMap, self).draw_line(start, end, colour)
        super(AtlasMap, self).draw_circle(start, 10, "blue")
        super(AtlasMap, self).draw_circle(end, 10, "blue")

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

def should_wrap_over_pacific(start, end, image):
    start_x   = start[0]
    end_x     = end[0]
    img_width = image.size[0]

    return abs(end_x - start_x) > (img_width / 2)

def coord_missing(start, end, coords):
    return not all(asys in coords for asys in [start,end])

def start_closer_to_RHS(start_x, img_width):
    return (img_width - start_x) < start_x
