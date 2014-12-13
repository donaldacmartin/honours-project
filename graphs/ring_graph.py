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

LayeredRingGraph

A subclass of RingGraph that also generates a connected graph of autonomous
systems in a series of rings, based on the number of connections that each AS
has to other ASs.
"""

class RingGraph(object):
    def __init__(self, width, height, asys_connections):
        self.asys_connections = {}
        self.asys_coordinates = {}
        
        for (start, end) in asys_connections:
            self.__add_connection(start, end)
            self.__add_connection(end, start)
        
        self.image = new("RGB", (width, height), "white")
        self.__calculate_asys_coordinates()

    def __add_connection(self, local_asys, foreign_asys):
        if local_asys not in self.asys_connections:
            self.asys_connections[local_asys] = set()
            
        self.asys_connections[local_asys].add(foreign_asys)
        
    def __calculate_asys_coordinates(self):
        angle_delta   = 360.0 / len(self.asys_connections)
        width, height = self.image.size
        
        centre = (width / 2, height / 2)
        radius = (width - 10) / 2
        
        angle = 0
        
        for asys in self.asys_connections:
            x = centre[0] - (radius * sin(angle))
            y = centre[1] - (radius * cos(angle))
            
            self.asys_coordinates[asys] = (x,y)
            angle += angle_delta
            
        self.__draw()
        self.image.save(self.filename, "PNG")
    
    def __draw(self):
        draw = Draw(self.image)
        
        for (asys, connections) in self.asys_connections.items():
            start_xy = self.asys_coordinates[asys]
            
            for connected_asys in connections:
                end_xy = self.asys_coordinates[connected_asys]
                draw.line([start_xy, end_xy], fill=128, width=1)
                
    def save(self, filename, filetype="PNG"):
        self.image.save(filename, filetype)

class LayeredRingGraph(RingGraph):
    def __calculate_asys_coordinates(self):
        angle_delta   = 360.0 / len(self.asys_connections)
        width, height = self.image.size
        
        centre = (width / 2, height / 2)
        
        most_cxns   = max([len(cxns) for cxns in self.asys_connections.values()])
        std_radius  = (width - 10) / 2
        radius_step = std_radius / most_cxns
        
        angle = 0
        
        for (asys, connections) in self.asys_connections.items():
            radius = std_radius - (len(connections) * radius_step)
            x = centre[0] - (radius * sin(angle))
            y = centre[1] - (radius * cos(angle))
            
            self.asys_coordinates[asys] = (x,y)
            angle += angle_delta
            
        self.draw()
        
    def __draw(self):
        draw = Draw(self.image)
        
        for (asys, connections) in self.asys_connections.items():
            start_xy = self.asys_coordinates[asys]
            
            for connected_asys in connections:
                end_xy = self.asys_coordinates[connected_asys]
                draw.line([start_xy, end_xy], fill=128, width=1)