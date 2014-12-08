#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from math import sin, cos
from Image import new
from ImageDraw import Draw

"""
RingGraph

Generates a connected graph of autonomous systems, stored in a ring. Each AS is
stored at a set radius.

StaggeredRingGraph

A subclass of RingGraph that also generates a connected graph of autonomous
systems in a series of rings, based on the number of connections that each AS
has to other ASs.
"""

class RingGraph(object):
    def __init__(self, filename, width, height):
        self.links  = {}
        self.plot_positions = {}
        self.filename = filename
        
        self.image  = new("RGB", (width, height), "white")
        
    def add_link(self, start, end):
        self.__add_cxn(start, end)
        self.__add_cxn(end, start)
    
    def __add_cxn(self, node, link):
        if node not in self.links:
            self.links[node] = set()
            
        self.links[node].add(link)
        
    def draw_graph(self):
        angle_delta   = 360.0 / len(self.links)
        width, height = self.image.size
        
        centre = (width / 2, height / 2)
        radius = (width - 10) / 2
        
        angle = 0
        
        for asys in self.links:
            x = centre[0] - (radius * sin(angle))
            y = centre[1] - (radius * cos(angle))
            
            self.plot_positions[asys] = (x,y)
            angle += angle_delta
            
        draw_lines(self.image, self.links, self.plot_positions)
        self.image.save(self.filename, "PNG")

class StaggeredRingGraph(RingGraph):
    def draw_graph(self):
        angle_delta   = 360.0 / len(self.links)
        width, height = self.image.size
        
        centre = (width / 2, height / 2)
        
        largest_no_cxns = max([len(self.links[asys]) for asys in self.links])
        standard_radius = (width - 10) / 2
        radius_step     = standard_radius / largest_no_cxns
        
        angle = 0
        
        for asys in self.links:
            radius = standard_radius - (len(self.links[asys]) * radius_step)
            x = centre[0] - (radius * sin(angle))
            y = centre[1] - (radius * cos(angle))
            
            self.plot_positions[asys] = (x,y)
            angle += angle_delta
        
        draw_lines(self.image, self.links, self.plot_positions)
        self.image.save(self.filename, "PNG")
        
def draw_lines(image, auto_systems, plot_positions):
    draw = Draw(image)
    
    for auto_sys in auto_systems:
        start_xy    = plot_positions[auto_sys]
        connections = auto_systems[auto_sys]
        
        for connection in connections:
            end_xy = self.plot_positions[connection]
            draw.line([start_xy, end_xy], fill=128, width=1)