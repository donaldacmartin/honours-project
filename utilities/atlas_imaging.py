#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from ImageDraw import Draw

def draw_connection(start, end, image, colour):
    draw_cursor = Draw(image)
    draw_cursor.line([start, end], fill=colour, width=1)
    
def draw_transpacfic_connection(start, end, image, colour):
    start_x, start_y      = start
    end_x, end_y          = end
    img_width, img_height = image.size
    draw_cursor           = Draw(image)
    
    dx = end_x - start_x
    dy = end_y - start_y
    
    line_1_x = img_width if start_closer_to_RHS(start_x, img_width) else 0    
    line_2_x = img_width - line_1_x
    lines_y  = start_y - (((line_1_x - start_x) / dx) * dy)
    
    draw_cursor.line([start, (line_1_x, lines_y)], fill=colour, width=1)
    draw_cursor.line([end, (line_2_x, lines_y)], fill=colour, width=1)
        
def start_closer_to_RHS(start_x, img_width):
    return (img_width - start_x) < start_x