#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

import logging

"""
GeoIPLookup

Provides an interface to convert an IP address into geographical information,
such as latlon coordinates or country & city information. Developed using CSV
data from MaxMind @ dev.maxmind.com/geoip/legacy/. Recommend to only generate
one of these instances for entires program, as setup is computationally intense.
"""

class GeoIPLookup(object):
    def __init__(self):
        self.geo_data  = read_into_table("data/locations.csv", location_parser)
        self.ip_blocks = read_into_table("data/blocks.csv", block_parser)
        
        self.block_start_ip = sorted(self.ip_blocks.keys())
        
    def get_latlon_for_ip(self, ip_address):
        try:
            data = get_ip_data(ip_address)
            return data["latitude"], data["longitude"]
        except NameError:
            logging.error("GeoIP: no latlon coordinates for " + ip_address)
            raise

    def get_country_for_ip(self, ip_address):
        try:
            data = get_ip_data(ip_address) 
            return data["country"]
        except NameError:
            logging.error("GeoIP: no country for " + ip_address)
            raise
    
    def __get_ip_data(self, ip_address):
        block    = self.__get_ip_block(ip_address)
        location = block["location"]
        return self.geo_data[location]
        
    def __get_ip_block(self, ip_address):
        ip_int = ip_to_int(ip_address)
        index  = next(n[0] for n in enumerate(self.block_start_ip) if n[1] > ip_int)
        block  = self.block_start_ip[index - 1]
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

def ip_to_int(ip_address):
    o = ip_address.split(".")
    
    o1 = 16777216 * int(o[0])
    o2 = 64436 * int(o[1])
    o3 = 256 * int(o[2])
    o4 = int(o[3])
    
    return o1 + o2 + o3 + o4

def location_parser(line):
    values       = line.split(",")
    location_id  = int(values[0])  
    lookup_table = {}
    
    # CSV format: locId,country,region,city,postcode,lat,lon,metroCode,areaCode

    lookup_table["country"]   = values[1]
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