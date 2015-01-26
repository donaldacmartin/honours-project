from __future__ import division
from graphs.base_graph import BaseGraph, DARK_RED
from utilities.parser.geoip import GeoIPLookup

GLOBAL        = ((90, 180), (-90,-180))
AFRICA        = ((36.08, -21.62), (-38.50, 50.45))
EUROPE        = ((61.16, -11.51), (35.63, 33.66))
NORTH_AMERICA = ((62.95, -167.52), (17.04, -52.56))
SOUTH_AMERICA = ((10.21, -92.64), (-54.94, -35.33))

class BaseAtlas(BaseGraph):
    def __init__(self, width, height, region=GLOBAL):
        super(BaseAtlas, self).__init__(width, height)

        self.geoip       = GeoIPLookup()
        self.region      = region
        self.asys_coords = {}

    # --------------------------------------------------------------------------
    # Resolving IP Addresses to XY-Coordinates
    # --------------------------------------------------------------------------

    def resolve_bgp_to_asys_coords(self, bgp_dump):
        for (asys, ip_addresses) in bgp_dump.asys_ip_address.items():
            coords = self.ip_addresses_to_coord(ip_addresses)

            if coords is not None:
                self.asys_coords[asys] = coords

    def ip_addresses_to_coord(self, ip_addresses):
        if len(ip_addresses) == 0:
            return None

        ip_address = ip_addresses.pop()
        lat,lon    = self.geoip.get_latlon_for_ip(ip_address)

        if any(coord is None for coord in [lat,lon]):
            return self.ip_addresses_to_coord(ip_addresses)
        else:
            return self.latlon_to_coords(lat,lon)

    # --------------------------------------------------------------------------
    # Draw Connections Between Autonomous Systems
    # --------------------------------------------------------------------------

    def draw_connections(self, connections, colour):
        for (start, end) in connections:
            if any(asys not in self.asys_coords for asys in [start, end]):
                continue

            start = self.asys_coords[start]
            end   = self.asys_coords[end]

            if self.is_transpacific_line(start, end):
                self.draw_transpacific_connection(start, end, colour)
            else:
                self.draw_line(start, end, colour)

    def is_transpacific_line(self, start, end):
        if self.region != GLOBAL:
            return False

        start_x   = start[0]
        end_x     = end[0]
        img_width = self.image.size[0]

        return abs(end_x - start_x) > (img_width / 2)

    def draw_transpacific_connection(self, start, end, colour):
        x1, y1 = start
        x2, y2 = end
        img_width, img_height = self.image.size

        dx = x2 - x1
        dy = y2 - y1

        x3 = img_width if (img_width - x1) > x1 else 0
        x4 = img_width - x3
        y3 = y4 = x1 - (((x3 - x1) / dx) * dy)

        self.draw_line(start, (x3, y3), colour)
        self.draw_line(end, (x4, y4), colour)

    # --------------------------------------------------------------------------
    # Draw Country Outlines
    # --------------------------------------------------------------------------

    def draw_international_boundaries(self):
        reader = Reader("utilities/data/country_outlines/countries")
        cursor = Draw(self.image)

        for point in reader.shapeRecords():
            points  = record.shape.points
            outline = [self.latlon_to_coords(lat, lon) for (lon, lat) in points]

            for i in range(1, len(outline)):
                self.draw_line(outline[i-1], outline[i], "black")

    # --------------------------------------------------------------------------
    # Converting Latitudes & Longitudes to xy-Coordinates
    # --------------------------------------------------------------------------

    def lat_to_y_coord(self, lat):
        img_height     = self.image.size[1]
        img_centre     = img_height / 2
        pixels_per_deg = img_height / 180
        return img_centre - (lat * pixels_per_deg)

    def lon_to_x_coord(self, lon):
        img_width      = self.image.size[0]
        img_centre     = img_width / 2
        pixels_per_deg = img_width / 360
        return img_centre + (lon * pixels_per_deg)

    def latlon_to_coords(self, lat, lon):
        img_width, img_height = self.image.size
        lim1_lat, lim1_lon    = self.region[0]
        lim2_lat, lim2_lon    = self.region[1]

        x, x1, x2 = [self.lon_to_x_coord(i) for i in [lon, lim1_lon, lim2_lon]]
        y, y1, y2 = [self.lat_to_y_coord(i) for i in [lat, lim1_lat, lim2_lat]]

        x_anchor = min(x1, x2)
        y_anchor = min(y1, y2)

        x_scale = img_width / abs(x2 - x1)
        y_scale = img_height / abs(y2 - y1)

        x = (x - x_anchor) * x_scale
        y = (y - y_anchor) * y_scale

        return (x,y)
