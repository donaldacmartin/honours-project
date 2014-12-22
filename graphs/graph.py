#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from Image import new
from ImageDraw import Draw

LIGHT_GREY  = (162,162,162)
LIGHT_GREEN = (59, 255, 134)
DARK_RED    = (255, 59, 59)

class Graph(object):
    def __init__(self, width, height):
        self.image = new("RGB", (width, height), "white")
        
    def draw_line(self, start, end, colour):
        cursor = Draw(self.image)
        cursor.line([start, end], fill=colour, width=1)
        
    def save(self, filename, filetype="PNG"):
        self.image.save(filename, filetype)