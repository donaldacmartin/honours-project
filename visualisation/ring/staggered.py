from math import sin, cos, radians, sqrt
from visualisation.base import BaseGraph, DARK_RED
from utilities.geoip import GeoIPLookup

class StaggeredRing(BaseGraph):
    def __init__(self, bgp_dump, width, height):
        super(StaggeredRing, self).__init__(width, height)
        self.geoip = GeoIPLookup()
        self.asys_coords = {}

        self.total_connections = self.sort_into_num_connections(bgp_dump.asys_connections)
        self.max_connections   = float(max(self.total_connections.itervalues()))

        for (asys, ip_addresses) in bgp_dump.asys_to_ip_addr.items():
            self.map_as_ip_to_circumference_pos(asys, ip_addresses)

        self.draw_markers()

        for (start, end) in bgp_dump.asys_connections:
            self.draw_connection(start, end)

    def sort_into_num_connections(self, asys_connections):
        lookup = {}

        for (start, end) in asys_connections:
            if start in lookup:
                lookup[start] += 1
            else:
                lookup[start] = 1

            if end in lookup:
                lookup[end] += 1
            else:
                lookup[end] = 1

        return lookup

    def map_as_ip_to_circumference_pos(self, as_num, ip_addresses):
        lon = self.get_longitude_for_ip_addrs(ip_addresses)

        if lon is None:
            return

        lon           = radians(lon)
        width, height = self.image.size
        radius_scale  = 1 - (self.total_connections[as_num] / self.max_connections)
        centre_x      = width / 2
        centre_y      = height / 2

        x = centre_x + ((centre_x * radius_scale) * cos(lon))
        y = centre_y + ((centre_y * radius_scale) * sin(lon))

        self.asys_coords[as_num] = (x,y)

    def get_longitude_for_ip_addrs(self, ip_addresses):
        while len(ip_addresses) > 0:
            try:
                ip_address = ip_addresses.pop()
                return self.geoip.get_latlon_for_ip(ip_address)[1] + 180
            except:
                continue

        return None

    def draw_markers(self):
        north_y  = 25
        centre_y = self.image.size[1] / 2
        south_y  = self.image.size[1] - 250

        east_x   = self.image.size[0] - 350
        centre_x = self.image.size[0] / 2
        west_x   = 25

        self.draw_text((centre_x, south_y), "GMT")
        self.draw_text((centre_x, north_y), "Intl Dateline")
        self.draw_text((east_x, centre_y), "E 90")
        self.draw_text((west_x, centre_y), "W 90")

    def draw_connection(self, start, end):
        if start not in self.asys_coords or end not in self.asys_coords:
            return

        start = self.asys_coords[start]
        end   = self.asys_coords[end]

        self.draw_line(start, end, DARK_RED)
