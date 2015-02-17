#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from bisect import bisect_left
from parser.ip_utils import ip_to_int

"""
GeoIPLookup

Provides an interface to convert an IP address into geographical information,
such as latlon coordinates or country & city information. Developed using CSV
data from MaxMind @ dev.maxmind.com/geoip/legacy/. Recommend to only generate
one of these instances for entires program, as setup is computationally intense.
"""

LOCATION_FILE = "utilities/data/locations.csv"
BLOCK_FILE    = "utilities/data/blocks.csv"

class GeoIPLookup(object):
    def __init__(self):
        self.geo_data       = read_into_table(LOCATION_FILE, location_parser)
        self.ip_blocks      = read_into_table(BLOCK_FILE, block_parser)
        self.iso_2to3       = load_iso_mappings()
        self.block_start_ip = sorted(self.ip_blocks.keys())

    def get_latlon_for_ip(self, ip_address):
        try:
            data = self._get_ip_data(ip_address)
            return data["latitude"], data["longitude"]
        except NameError:
            logging.error("GeoIP: no latlon coordinates for " + ip_address)
            return None

    def get_country_for_ip(self, ip_address):
        try:
            data = self._get_ip_data(ip_address)
            return self.iso_2to3[data["country"]]
        except:
            return None

    def _locate_block(self, ip_int):
        i = bisect_left(self.block_start_ip, ip_int)

        if i:
            return self.block_start_ip[i-1]

        raise ValueError

    def _get_ip_data(self, ip_address):
        block    = self._get_ip_block(ip_address)
        location = block["location"]
        return self.geo_data[location]

    def _get_ip_block(self, ip_address):
        ip_int = ip_to_int(ip_address, True)
        block  = self._locate_block(ip_int)
        return self.ip_blocks[block]

# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------
def read_into_table(filename, line_parser):
    f = open(filename, "r")
    database = {}
    line = f.readline()[:-1]

    while line != "":
        try:
            key, entry = line_parser(line)
            database[key] = entry
        except:
            pass
        line = f.readline()[:-1]

    f.close()
    return database

def location_parser(line):
    values       = line.split(",")
    location_id  = int(values[0])
    lookup_table = {}

    # CSV format: locId,country,region,city,postcode,lat,lon,metroCode,areaCode

    lookup_table["country"]   = values[1].replace("\"", "")
    lookup_table["region"]    = values[2]
    lookup_table["city"]      = values[3]
    lookup_table["latitude"]  = float(values[5])
    lookup_table["longitude"] = float(values[6])

    return location_id, lookup_table

def block_parser(line):
    line         = line.replace("\"", "")
    values       = line.split(",")
    start_ip     = int(values[0])
    lookup_table = {}

    # CSV format: startIpNum, endIpNum, locId

    lookup_table["end_ip"]   = int(values[1])
    lookup_table["location"] = int(values[2])

    return start_ip, lookup_table

def load_iso_mappings():
    csv_file = open("utilities/data/fips2iso.txt")
    record   = csv_file.readline()
    iso2to3  = {}

    while record != "":
        if not record.startswith("#"):
            iso2to3 = parse_iso_mapping(record, iso2to3)

        record = csv_file.readline()

    csv_file.close()
    return iso2to3

def parse_iso_mapping(record, iso2to3):
    iso2 = record.split(",")[1]
    iso3 = record.split(",")[2]

    iso2to3[iso2] = iso3
    return iso2to3
