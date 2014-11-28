import Image, ImageDraw
from math import sin, cos

"""
http://www.effbot.org/imagingbook/imagedraw.htm
"""

class EasyGraph():
    def __init__(self):
        self.nodes  = {}
        self.plots  = {}
        self.lines  = []
        
        self.width  = 1024
        self.height = 768
        
        self.image = Image.new("RGB", (self.width, self.height), "white")
        
    def add_link(self, id, link):
        if int(id) not in self.nodes:
            self.nodes[int(id)] = []
            self.nodes[int(id)].append(int(link))
        else:
            self.nodes[int(id)].append(int(link))
            
        if int(link) not in self.nodes:
            self.nodes[int(link)] = []
            self.nodes[int(link)].append(int(id))
        else:
            self.nodes[int(link)].append(int(id))
        
    def draw_graph(self):
        self.__draw_nodes()
        self.__draw_lines()
        
        draw = ImageDraw.Draw(self.image)
        
        for line in self.lines:
            draw.line((line[0][0], line[0][1], line[1][0], line[1][1]), fill=128)
            
        self.image.save("lol", "PNG")
            
    def __draw_nodes(self):
        angle_delta = 360 / len(self.nodes)
        
        centre = (self.width / 2, self.height / 2)
        radius = self.width / 3
        
        angle = 0
        
        for i in range(len(self.nodes)):
            x = centre[0] - (radius * sin(angle))
            y = centre[1] - (radius * cos(angle))
            angle += angle_delta
            self.plots[i] = (x,y)
            
    def __draw_lines(self):
        for i in self.nodes:
            for asys in self.nodes[i]:
                start = self.plots[i]
                end   = self.plots[asys]
                self.lines.add(start, end)