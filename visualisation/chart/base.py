#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from visualisation.base import BaseGraph

"""
Base Chart

A chart class that allows some basic operations common to all deriving charts
(eg drawing an axis). Subclass of Base Graph allowing save and line drawing.
"""

class BaseChart(BaseGraph):
    def __init__(self, width, height):
        super(BaseChart, self).__init__(width, height)

    def draw_axes(self):
        img_width, img_height = self.image.size

        origin     = (img_width * 0.1, img_height * 0.9)
        x_axis_end = (img_width * 0.1, img_height * 0.1)
        y_axis_end = (img_width * 0.9, img_height * 0.9)

        self.draw_line(origin, x_axis_end, width=10)
        self.draw_line(origin, y_axis_end, width=10)
