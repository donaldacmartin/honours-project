#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from Image import new

class Graph(object):
    def __init__(self, width, height):
        self.image = new("RGB", (width, height), "white")
        
    def save(self, filename, filetype="PNG"):
        self.image.save(filename, filetype)