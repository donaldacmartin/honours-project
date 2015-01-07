#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from graphs.graph import Graph
from utilities.geoip import GeoIPLookup

class AddressesPerCapitaGraph(Graph):
    def __init__(self, width, height, bgp_dump):
        super(RingGraph, self).__init__(width, height)
        countries = self._sort_bgp_data_into_countries(bgp_dump)


    def _sort_bgp_data_into_countries(self, bgp_dump):
        ip_addresses = bgp_dump.as_to_ip_address
        alloc_sizes  = bgp_dump.as_alloc_size
        geo_ip       = GeoIPLookup()
        countries    = {}

        for (asys, alloc_size) in alloc_sizes:
            ip_address = ip_addresses[asys]
            country    = geo_ip.get_country_for_ip(ip_address)

            if country not in countries:
                countries[country] = 0

            countries[country] += alloc_size

        return countries

    def _load_population_data(self):
        pass

    def _draw_countries(self, pop_lookup):
        reader = Reader("utilities/data/country_outlines/countries")
        draw = Draw(self.image)

        for record in reader.shapeRecords():
            points       = record.shape.points
            country_code = record.record[23]
            outline      = []

            for (lon, lat) in points:
                x, y = scale_coords((lat, lon), self.region, self.image)
                outline.append((x,y))

            for i in range(1, len(outline)):
                draw.line([outline[i-1], outline[i]], fill="black", width=3)
