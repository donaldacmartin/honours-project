#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from images2gif import writeGif
from atlas_map import map_lon_to_x_coord, map_lat_to_y_coord
from geoip import GeoIPLookup
from Image import new
from ImageDraw import Draw
from file import *
import logging
from threading import Thread

class MonthlyTimeline(object):
    def __init__(self, files):
        self.files_to_parse = files

        self.bgp_dumps = {}
        self.images    = {}

        self.__launch_bgp_threads()
        
    def __launch_bgp_threads(self):
        bgp_threads = []

        for bgp_file in self.files_to_parse:
            thr = Thread(target=bgp_dump_thread, args=(bgp_file,self.bgp_dumps,))
            thr.start()
            bgp_threads.append(thr)
            
        for bgp_thread in bgp_threads:
            bgp_thread.join()
            
        self.__launch_graph_threads()
            
    def __launch_graph_threads(self):
        graph_threads = []
        
        for i in range(1, len(self.files_to_parse), 2):
            prev_dump = self.bgp_dumps[self.files_to_parse[i-1]]
            curr_dump = self.bgp_dumps[self.files_to_parse[i]]
            
            name = self.files_to_parse[i]
            
            args = (prev_dump, curr_dump, 2000, 1000, self.images, name,)
            thr  = Thread(target=graph_generator_thread, args=args)
            
            thr.start()
            graph_threads.append(thr)
            
        for thr in graph_threads:
            thr.join()
            
        self.__write_file()
            
    def __write_file(self):
        images = []
        
        for i in range(1, len(self.files_to_parse), 2):
            images.append(self.images[self.files_to_parse[i]])
            
        writeGif("big.gif", images, duration=0.5)

def bgp_dump_thread(filepath, dump_location):
    bgpdump = BGPDumpExecutor(file_path)
    dump_location[filepath] = bgpdump
    
def graph_generator_thread(prev_dump, curr_dump, width, height, images, name):
    map = ChronologicalAtlasMap(width, height)
    merged_as_nums = merge_as_databases(prev_dump, curr_dump)
    
    for auto_sys in merged_as_nums:
        map.add_auto_sys_ip(auto_sys, merged_as_nums[auto_sys])
        
    added, removed, unchanged = sort_connections(prev_dump, curr_dump)
    
    for (start, end) in added:
        chrono.add_new_link(start, end)
        
    for (start, end) in removed:
        chrono.add_removed_link(start, end)
        
    for (start, end) in unchanged:
        chrono.add_unchanged_link(start, end)
        
    images[name] = dumpmap.draw()
    
def merge_as_databases(prev_dump, curr_dump):
    prev = prev_dump.ip_addresses
    curr = curr_dump.ip_addresses
    
    return dict(list(prev.items()) + list(curr.items()))

def sort_connections(prev_dump, curr_dump):
    prev_cxns = prev_dump.connections
    curr_cxns = curr_dump.connections
    
    added     = curr_cxns.difference(prev_cxns)
    removed   = prev_cxns.difference(curr_cxns)
    unchanged = curr_cxns.intersection(prev_cxns)
    
    return added, removed, unchanged
    
# ------------------------------------------------------------------------------

class ChronologicalAtlasMap(object):
    def __init__(self, width, height):
        self.connections_added     = set()
        self.connections_removed   = set()
        self.connections_unchanged = set()
        
        self.asys_coordinates      = {}
        
        self.geoip = GeoIPLookup()
        self.image = new("RGB", (width, height), "white")
        
    def add_auto_sys_ip(self, as_num, ip_address):
        if int(as_num) in self.asys_coordinates:
            return
            
        try:
            lat,lon       = self.geoip.get_latlon_for_ip(ip_address)
            as_num        = int(as_num)
            width, height = self.image.size
            
            x = map_lon_to_x_coord(lon, width)
            y = map_lat_to_y_coord(lat, height)
            
            self.asys_coordinates[as_num] = (x,y)
        except:
            logging.warning("AtlasMap: unable to add " + str(as_num))
        
    def draw(self):
        draw_cursor = Draw(self.image)
        
        for (start, end) in self.connections_unchanged:
            self.__draw_link(start, end, draw_cursor, (212,212,212))
                
        for (start, end) in self.connections_removed:
            self.__draw_link(start, end, draw_cursor, (128,0,0))
                
        for (start, end) in self.connections_added:
            self.__draw_link(start, end, draw_cursor, (55,237,91))
            
        return self.image
    
    def __draw_link(self, start, end, draw, colour_value):
        try:
            start_xy = self.asys_coordinates[start]
            end_xy   = self.asys_coordinates[end]
            draw.line([start_xy, end_xy], fill=colour_value, width=1)
        except KeyError as e:
            logging.warning("AtlasMap: AS" + str(e) + " not in list of coords")