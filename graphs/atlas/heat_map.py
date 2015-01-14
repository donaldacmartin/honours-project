#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from graphs.graph import Graph
from utilities.geoip import GeoIPLookup
from utilities.population import get_global_population_database
from atlas_map import GLOBAL, map_lon_to_x_coord, map_lat_to_y_coord

"""
HeatMap

An object that converts a BGP dump into an atlas map, where each country is
shaded according to the number of IPv4 addresses per capita.

Goals
 - Break BGP data into countries
 - Load population data for each country
 - Load shapefiles
 - Draw and shade
"""

class HeatMap(Graph):
    def __init__(self, bgp_dump, region=GLOBAL, width=1920, height=1080):
        super(HeatMap, self).__init__(width, height)

        year       = bgp_dump.date_time_stamp[0]
        allocs     = self._sort_bgp_into_countries(bgp_dump)
        pops       = get_global_population_database()
        per_capita = self._get_alloc_size_per_capita(allocs, pops, year)
        shades     = self._convert_figures_to_shades(per_capita)
        print("Got shades")

        self._draw(region, shades)

    def _sort_bgp_into_countries(self, bgp_dump):
        geoip = GeoIPLookup()
        national_total_alloc = {}

        for asys, alloc_size in bgp_dump.as_alloc_size.iteritems():
            try:
                ip_addr = bgp_dump.as_to_ip_address[asys]
                country = geoip.get_country_for_ip(ip_addr)
                national_total_alloc[country] = alloc_size
            except:
                print("No country data for IP address " + ip_addr)
                continue

        return national_total_alloc

    def _get_alloc_size_per_capita(self, allocations, populations, year):
        per_capita = {}

        for country, alloc_size in allocations.iteritems():
            try:
                population = populations[country][year]
                per_capita[country] = alloc_size / float(population)
            except:
                continue

        return per_capita

    def _convert_figures_to_shades(self, per_capita):
        max_per_capita = max(per_capita.values())
        min_per_capita = min(per_capita.values())
        scale          = 255.0 / (max_per_capita - min_per_capita)
        shades         = {}

        for country, value in per_capita.iteritems():
            shades[country] = (value - min_per_capita) * scale

        return shades

    def _draw(self, region, shades):
        reader = Reader("utilities/data/country_outlines/countries")
        cursor = Draw(self.image)

        ((x1, y1), (x2, y2)) = self._convert_region_to_coords(region)

        x_anchor = min(x1, x2)
        y_anchor = min(y1, y2)

        x_scale = img_width / abs(x2 - x1)
        y_scale = img_height / abs(y2 - y1)

        for record in reader.shapeRecords():
            points  = record.shape.points
            country = record.record[23]
            outline = []
            colour  = (shades[country], 0, 0)

            for (lon, lat) in points:
                x = (map_lon_to_x_coord(lon, self.image.size[0]) - x_anchor) * x_scale
                y = (map_lat_to_y_coord(lat, self.image.size[1]) - y_anchor) * y_scale

            cursor.polygon(outline, fill=colour)

    def _convert_region_to_coords(self, region):
        x1 = map_lon_to_x_coord(region[0][1], self.image.size[0])
        x2 = map_lon_to_x_coord(region[1][1], self.image.size[0])

        y1 = map_lat_to_y_coord(region[0][0], self.image.size[1])
        y2 = map_lat_to_y_coord(region[1][0], self.image.size[1])

        return ((x1, y1), (x2, y2))
