#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from __future__ import division
from graphs.graph import Graph
from graphs.atlas.atlas_map import GLOBAL, scale_coords
from utilities.geoip import GeoIPLookup
from utilities.population import get_global_population_database
from utilities.shapefile import Reader
from ImageDraw import Draw

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

        self.geoip  = GeoIPLookup()
        self.bgp    = bgp_dump
        self.region = region

        year        = self.bgp.date_time_stamp[0]
        countries   = self._break_bgp_into_countries()
        populations = get_global_population_database()
        per_capita  = self._per_capita(countries, populations, year)
        shades      = self._shade_countries(per_capita)
        self._draw_map(shades)

    def _break_bgp_into_countries(self):
        countries = {}

        for (asys, size) in self.bgp.asys_size.items():
            country = self._get_country_for_asys(asys)

            if country not in countries:
                countries[country] = 0

            countries[country] += size

        return countries

    def _get_country_for_asys(self, asys):
        ip_addresses = self.bgp.asys_ip_address[asys]

        for ip_address in ip_addresses:
            country = self.geoip.get_country_for_ip(ip_address)

            if country is not None:
                break

        return country

    def _per_capita(self, countries, populations, year):
        per_capita = {}

        for (country, address_space) in countries.items():
            if country in populations and year in populations[country]:
                population           = populations[country][year]
                addresses_per_capita = address_space / population
                per_capita[country]  = addresses_per_capita

        return per_capita

    def _shade_countries(self, per_capita):
        max_per_capita = max(per_capita.values())
        min_per_capita = min(per_capita.values())
        dif_per_capita = max_per_capita - min_per_capita

        shades         = {}

        for (country, value) in per_capita.items():
            value = 1 - ((value - min_per_capita) / dif_per_capita)
            shade = int(value * 255)
            shades[country] = (255, shade, shade)

        return shades

    def _draw_map(self, shades):
        reader = Reader("utilities/data/country_outlines/countries")
        draw = Draw(self.image)

        for record in reader.shapeRecords():
            country = record.record[9]
            points  = record.shape.points
            outline = []

            if country not in shades:
                continue

            for (lon, lat) in points:
                x, y = scale_coords((lat, lon), self.region, self.image)
                outline.append((x,y))

            draw.polygon(outline, fill=shades[country])
