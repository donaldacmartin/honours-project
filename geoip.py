#!/usr/bin/env python
#C:\Python27\ArcGIS10.1\python.exe

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

"""
Layer for GeoLite MaxMind files:
http://dev.maxmind.com/geoip/legacy/geolite/
"""
class GeoIPLookup(object):
    def __init__(self, loc_filename, block_filename):
        self.locations = read_file_into_database(loc_filename, location_parser)
        self.blocks    = read_file_into_database(block_filename, block_parser)
        
        self.start_ip = sorted(self.blocks.keys())
        
    def get_latlon_for_ip(self, ip_address):
        ip_int = ip_to_int(ip_address)
        
        index = next(n[0] for n in enumerate(self.start_ip) if n[1] > ip_int) - 1
        block_entry = self.start_ip[index]
        
        location = self.blocks[block_entry]["location"]
        lat = self.locations[location]["latitude"]
        lon = self.locations[location]["longitude"]
        
        return lat,lon

# ------------------------------------------------------------------------------
# File Handling
# ------------------------------------------------------------------------------
def read_file_into_database(filename, line_parser):
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

# ------------------------------------------------------------------------------
# Converting between IP address strings and integer representations
# ------------------------------------------------------------------------------
def ip_to_int(ip_address):
    o = ip_address.split(".")
    
    o1 = 16777216 * int(o[0])
    o2 = 64436 * int(o[1])
    o3 = 256 * int(o[2])
    o4 = int(o[3])
    
    return o1 + o2 + o3 + o4
    
def int_to_ip(number):
    o1 = str(int(number / 16777216) % 256)
    o2 = str(int(number / 65536) % 256)
    o3 = str(int(number / 256) % 256)
    o4 = str(int(number) % 256)
    return ".".join([o1, o2, o3, o4])

# ------------------------------------------------------------------------------
# Parsing CSV data into dictionaries
# ------------------------------------------------------------------------------
def location_parser(line):
    values       = line.split(",")
    location_id  = int(values[0])  
    lookup_table = {}
    
    # CSV format: locId,country,region,city,postcode,lat,lon,metroCode,areaCode

    lookup_table["country"]   = values[1]
    lookup_table["region"]    = values[2]
    lookup_table["city"]      = values[3]
    lookup_table["latitude"]  = int(values[5])
    lookup_table["longitude"] = int(values[6])
    
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