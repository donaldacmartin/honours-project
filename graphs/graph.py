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
        
    def draw_line2(self, start, end, colour):
        cursor = Draw(self.image)
        cursor.line([start, end], fill=colour, width=1)
        
    def draw_line(self, start, end, colour):
        img_pixels = self.image.load()
        x0, y0 = start
        x1, y1 = end
        
        dx = x1 - x0
        dy = y1 - y0
        
        D = (2 * dy) - dx
        img_pixels[x0, y0] = colour
        
        y = y0
        
        for x in range(x0 + 1, x1):
            if D > 0:
                y += 1
                img_pixels[x, y] = colour
                D += (2 * dy) - (2 * dx)
            else:
                img_pixels[x, y] = colour
                D += (2 * dy)
        
    def save(self, filename, filetype="PNG"):
        self.image.save(filename, filetype)