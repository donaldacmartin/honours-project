#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from Image import new, ANTIALIAS
from ImageDraw import Draw
from ImageFont import truetype

LIGHT_GREY  = (162,162,162)
LIGHT_GREEN = (59, 255, 134)
DARK_RED    = (255, 59, 59)

class BaseGraph(object):
    def __init__(self, width, height):
        self.image  = new("RGB", (width * 10, height * 10), "white")
        self.cursor = Draw(self.image)
        self._initialise_text_font()

    def _initialise_text_font(self):
        font_path     = "utilities/data/font_arial.ttf"
        self.arial100 = truetype(font_path, 16)

    def draw_line(self, start, end, colour=DARK_RED, width=1):
        self.cursor.line([start, end], fill=colour, width=width)

    def draw_circle(self, (x,y), r, colour=DARK_RED):
        self.cursor.ellipse((x-r, y-r, x+r, y+r), fill=colour)

    def draw_text(self, xy, text, colour=DARK_RED):
        self.cursor.text(xy, text, font=self.arial100, fill=colour)

    def save(self, filename, filetype="PNG"):
        x, y = self.image.size

        resized_img = self.image.resize((x / 10, y / 10), ANTIALIAS)
        resized_img.save(filename, filetype)
