#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from graphs.graph import Graph, GLOBAL
from utilities.geoip import GeoIPLookup
from utilities.population import get_global_population_database

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

        self.geoip = GeoIPLookup()
        self.bgp   = bgp_dump

        year        = self.bgp.date_time_stamp[0]
        countries   = self._break_bgp_into_countries()
        populations = get_global_population_database()

    def _break_bgp_into_countries():
        countries = []

        for (asys, size) in self.bgp.asys_size.items():
            country = self._get_country_for_asys(asys)

            if country not in countries:
                countries[country] = 0

            countries[country] += size

        return countries

    def _get_country_for_asys(asys):
        ip_addresses = self.bgp.asys_ip_address[asys]

        for ip_address in ip_addresses:
            country = self.geoip.get_country_for_ip(ip_address)

            if country is not None:
                break

        return country
