#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

"""
Layer for GeoLite MaxMind files:
http://dev.maxmind.com/geoip/legacy/geolite/
"""
class GeoIPLookup(object):
    def __init__(self, loc_file, block_file):
        loc_file   = "data/locations.csv"
        block_file = "data/blocks.csv"
        
        self.location_data  = read_into_table("data/locations.csv", location_parser)
        self.ip_blocks      = read_into_table(block_file, block_parser)
        self.block_start_ip = sorted(self.blocks.keys())
        
    def get_latlon_for_ip(self, ip_addr):
        try:
            data = get_ip_data(ip_addr, self.block_start_ip, self.ip_blocks, self.location_data)
            return data["latitude"], data["longitude"]
        except NameError:
            raise

    def get_country_for_ip(self, ip_addr):
        try:
            data = get_ip_data(ip_addr, self.block_start_ip, self.ip_blocks, self.location_data) 
            return data["country"]
        except NameError:
            raise

# ------------------------------------------------------------------------------
# Getting IP address data from database
# ------------------------------------------------------------------------------
def get_ip_data(ip_address, start_ips, blocks, locations):
    try:
        ip_int = ip_to_int(ip_address)
        index  = next(n[0] for n in enumerate(start_ips) if n[1] > ip_int) - 1
        block  = starting_ips[index]
        
        location = blocks[block_entry]["location"]
        return locations[location]
    except:
        raise NameError("Unable to locate " + ip_address + " in database")

# ------------------------------------------------------------------------------
# File Handling
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