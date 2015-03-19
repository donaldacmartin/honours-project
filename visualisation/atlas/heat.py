from __future__ division
from base import BaseAtlas, GLOBAL
from utilities.population import get_global_population_database
from utilities.shapefile import Reader
from ImageDraw import Draw

class HeatAtlas(BaseAtlas):
    def __init__(self, bgp_dump, width=1920, height=1080, region=GLOBAL):
        super(HeatAtlas, self).__init__(width, height, region)

        self.bgp    = bgp_dump
        year        = self.bgp.datetime.year
        countries   = self.break_bgp_into_countries()
        populations = get_global_population_database()
        per_capita  = self.per_capita(countries, populations, year)
        shades      = self.shade_countries(per_capita)

        print(shades)
        self.draw_map(shades)

    def break_bgp_into_countries(self):
        countries = {}

        for (asys, size) in self.bgp.asys_size.items():
            country = self.get_country_for_asys(asys)

            if country not in countries:
                countries[country] = 0

            countries[country] += size

        return countries

    def get_country_for_asys(self, asys):
        ip_addresses = self.bgp.asys_to_ip_addr[asys]
        country      = None

        for ip_address in ip_addresses:
            try:
                country = self.geoip.get_country_for_ip(ip_address)
                break
            except:
                continue

        return country

    def per_capita(self, countries, populations, year):
        per_capita = {}

        for (country, address_space) in countries.items():
            if country in populations and year in populations[country]:
                population           = populations[country][year]
                addresses_per_capita = address_space / population
                per_capita[country]  = addresses_per_capita

        return per_capita

    def shade_countries(self, per_capita):
        max_per_capita = max(per_capita.values())
        min_per_capita = min(per_capita.values())
        dif_per_capita = max_per_capita - min_per_capita

        shades         = {}

        for (country, value) in per_capita.items():
            value = 1 - ((value - min_per_capita) / dif_per_capita)
            shade = int(value * 255)
            shades[country] = (255, shade, shade)

        return shades

    def draw_map(self, shades):
        reader = Reader("utilities/data/country_outlines/countries")
        draw = Draw(self.image)

        for record in reader.shapeRecords():
            country = record.record[9]
            points  = record.shape.points
            outline = []

            if country not in shades:
                continue

            for (lon, lat) in points:
                x, y = self.latlon_to_coords(lat, lon)
                outline.append((x,y))

            draw.polygon(outline, fill=shades[country])
