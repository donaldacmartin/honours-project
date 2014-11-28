import Image, ImageDraw

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
        
    def add_link(id, link):
        if int(id) in self.nodes:
            self.nodes[int(id)] = []
            self.nodes[int(id)].append(link)
        else:
            self.nodes[int(id)].append(link)
        
    def draw_graph(width, height):
        self.__draw_nodes()
        self.__draw_lines()
        
        draw = ImageDraw.Draw(im)
        
        for line in self.lines:
            draw.line((line[0][0], line[0][1], line[1][0], line[1][1]), fill=128)
            
        self.image.save("lol", "PNG")
            
    def __draw_nodes():
        angle_delta = 360 / len(self.nodes)
        
        centre = (self.width / 2, self.height / 2)
        radius = self.width / 3
        
        angle = 0
        
        for i in range(len(self.nodes)):
            x = centre[0] - (radius * sin(angle))
            y = centre[1] - (radius * cos(angle))
            angle += angle_delta
            self.plots[i] = (x,y)
            
    def __draw_lines():
        for i in range(len(self.nodes)):
            for asys in self.nodes[i]:
                start = self.plots[i]
                end   = self.plots[asys]
                self.lines.add(start, end)