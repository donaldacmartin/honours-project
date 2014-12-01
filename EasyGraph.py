import Image, ImageDraw
from math import sin, cos

"""
http://www.effbot.org/imagingbook/imagedraw.htm
"""
     
class RingGraph():
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
        angle_delta = float(360) / float(len(self.links))
        centre = (self.width / 2, self.height / 2)
        radius = self.width / 3
        
        angle = float(0)
        
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
        max_cxns = self.find_max()
        
        angle_delta = float(360) / float(len(self.links))
        centre = (self.width / 2, self.height / 2)
        max_radius = self.width / 3
        
        angle = float(0)
        
        for asys in self.links:
            radius = max_radius * (float(len(self.links[asys])) / max_cxns)
            print(radius)
            
            x = centre[0] - (radius * sin(angle))
            y = centre[1] - (radius * cos(angle))
            
            self.plot_positions[asys] = (x,y)
            angle += angle_delta
            
        self.__draw_lines()
        self.image.save("staggered.png", "PNG")
        
    def find_max(self):
        current_max = 0
        
        for asys in self.links:
            if len(self.links[asys]) > current_max:
                current_max = len(self.links[asys])
        
        return current_max
        
    def __draw_lines(self):
        draw = ImageDraw.Draw(self.image)
        
        for asys in self.links:
            for cxns in self.links[asys]:
                start = self.plot_positions[asys]
                end   = self.plot_positions[cxns]
                draw.line((start[0], start[1], end[0], end[1]), fill=128, width=1)