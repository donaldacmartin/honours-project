from __future__ import division
from base import BaseChart
from parser.mrt import MRTParser
from parser.cisco import CiscoParser
from utilities.file.search import FileBrowser
from utilities.parser.ip_utils import ip_to_int, cidr_to_int, get_reserved_blocks
from graphs.base import DARK_RED, LIGHT_GREY

DEFAULT = ("0.0.0.0", "255.255.255.255")
TESTING = ("4.0.0.0", "4.255.255.255")

class YearlyAllocatedBlocks(BaseChart):
    def __init__(self, bgp_dumps, bounds=DEFAULT, width=1920, height=1080):
        super(YearlyAllocatedBlocks, self).__init__(width, height)
        self.base_ip  = ip_to_int(bounds[0])
        self.limit_ip = ip_to_int(bounds[1])
        self.ip_range = self.limit_ip - self.base_ip

        img_height = self.image.size[1]
        row_diff   = (0.8 * img_height) / len(bgp_dumps)
        row_y      = img_height * 0.1

        for bgp_dump in bgp_dumps:
            blocks = bgp_dump.visible_blocks
            blocks = [block for block in blocks if self.block_in_range(block)]
            self.draw_bar(blocks, row_y)
            self.draw_reserved_blocks(row_y)
            self.draw_year_label(bgp_dump.date_time_stamp[0], row_y)
            row_y += row_diff

        self.draw_axes()
        self.draw_markers()

    def block_in_range(self, block):
        ip = block[0]
        return self.base_ip <= ip <= self.limit_ip

    def draw_bar(self, blocks, row_y, colour=DARK_RED):
        for (ip, cidr) in blocks:
            start_x = self.scale_ip_to_length(ip)
            end_x   = self.scale_ip_to_length(ip + cidr_to_int(cidr))
            self.draw_line((start_x, row_y), (end_x, row_y), colour, width=100)

    def draw_year_label(self, year, row_y):
        img_width = self.image.size[0]
        pos       = (0.05 * img_width, row_y)
        text      = str(year)
        self.draw_text(pos, text)

    def scale_ip_to_length(self, ip):
        img_width  = self.image.size[0]
        x_pos      = (ip - self.base_ip) / self.ip_range
        scaled_pos = (x_pos * (img_width * 0.8)) + (img_width * 0.1)
        return scaled_pos

    def draw_reserved_blocks(self, row_y):
        blocks = get_reserved_blocks()
        blocks = [block for block in blocks if self.block_in_range(block)]
        self.draw_bar(blocks, row_y, LIGHT_GREY)

    def draw_markers(self):
        img_width, img_height = self.image.size
        x_diff  = (img_width * 0.8) / 255
        x_pos   = img_width * 0.1
        y_min   = img_height * 0.1
        y_max   = img_height * 0.9
        y_label = img_height * 0.92

        for i in range(0, 255):
            self.draw_line((x_pos, y_min), (x_pos, y_max), DARK_GREY, width=2)

            if i % 10 == 0:
                self.draw_rotated_text((x_pos, y_label), str(i) + ".0.0.0")

            x_pos += x_diff
