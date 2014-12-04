import Image, ImageDraw
from math import sin, cos

"""
http://www.effbot.org/imagingbook/imagedraw.htm
"""
     
class RingGraph(object):
    def __init__(self, width, height):
        self.links  = {}
        self.plot_positions = {}
        
        self.width  = width
        self.height = height
        self.image  = Image.new("RGB", (width, height), "white")
        
    def add_link(self, start, end):
        self.__add_cxn(start, end)
        self.__add_cxn(end, start)
    
    def __add_cxn(self, node, link):
        if node not in self.links:
            self.links[node] = set()
            
        self.links[node].add(link)
        
    def draw_graph(self):
        angle_delta = 360.0 / len(self.links)
        centre = (self.width / 2, self.height / 2)
        radius = (self.width - 10) / 2
        
        angle = 0
        
        for asys in self.links:
            x = centre[0] - (radius * sin(angle))
            y = centre[1] - (radius * cos(angle))
            
            self.plot_positions[asys] = (x,y)
            angle += angle_delta
            
        self.__draw_lines()
        self.image.save("ring.png", "PNG")
            
    def __draw_lines(self):
        draw = ImageDraw.Draw(self.image)
        
        for asys in self.links:
            for cxns in self.links[asys]:
                start = self.plot_positions[asys]
                end   = self.plot_positions[cxns]
                draw.line((start[0], start[1], end[0], end[1]), fill=128, width=1)
                
class StaggeredRingGraph(RingGraph):
    def draw_graph(self):
        angle_delta = 360.0 / len(self.links)
        centre = (self.width / 2, self.height / 2)
        
        largest_no_cxns = max([len(self.links[asys]) for asys in self.links])
        standard_radius = (self.width - 10) / 2
        radius_step     = standard_radius / largest_no_cxns
        
        angle = 0
        
        for asys in self.links:
            radius = standard_radius - (len(self.links[asys]) * radius_step)
            x = centre[0] - (radius * sin(angle))
            y = centre[1] - (radius * cos(angle))
            
            self.plot_positions[asys] = (x,y)
            angle += angle_delta
            
        __draw_lines()
        self.image.save("staggered-ring.png", "PNG")