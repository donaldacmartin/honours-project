from __future__ import division
from base import BaseChart
from utilities.parser.mrt import MRTParser
from utilities.parser.cisco import CiscoParser
from utilities.file.search import FileBrowser
from utilities.parser.ip_utils import ip_to_int, cidr_to_int

DEFAULT = ("0.0.0.0", "255.255.255.255")
TESTING = ("4.0.0.0", "4.255.255.255")

class YearlyAllocatedBlocks(BaseChart):
    def __init__(self, bgp_dumps, bounds=DEFAULT, width=1920, height=1080):
        super(YearlyAllocatedBlocks, self).__init__(width, height)
        self.draw_axes()
        self.draw_markers()

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
            self.draw_year_label(bgp_dump.date_time_stamp[0])
            row_y += row_diff

    def block_in_range(self, block):
        ip = block[0]
        return self.base_ip <= ip <= self.limit_ip

    def draw_bar(self, blocks, row_y):
        for (ip, cidr) in blocks:
            start_x = self.scale_ip_to_length(ip)
            end_x   = self.scale_ip_to_length(ip + cidr_to_int(cidr))
            self.draw_line((start_x, row_y), (end_x, row_y), width=100)

    def draw_year_label(self, year, row_y):
        img_width = self.image.size[0]
        pos       = (0.05 * image_width, row_y)
        text      = str(year)
        self.draw_text(pos, text)

    def scale_ip_to_length(self, ip):
        img_width  = self.image.size[0]
        x_pos      = (ip - self.base_ip) / self.ip_range
        scaled_pos = (x_pos * (img_width * 0.8)) + (img_width * 0.1)
        return scaled_pos

    def draw_markers(self):
        delta  = (self.image.size[0] * 0.8) / 255
        cursor = self.image.size[0] * 0.1

        for i in range(0, 255):
            self.draw_line((cursor, self.image.size[1] * 0.9), (cursor, self.image.size[1] * 0.1), width=5)
            cursor += delta

if __name__ == "__main__":
    root_dir = "/nas05/users/csp/routing-data/archive.routeviews.org"
    database = FileBrowser(root_dir)
    years    = []

    for year in range(1997, 1998):
        years.append(database.get_year_end_files(year))

    years   = [year for year in years if year is not None]
    parsers = [MRTParser(filename[0]) if "rib" in filename[0] else CiscoParser(filename[0]) for filename in years]

    y = YearlyAllocatedBlocks(parsers)
    y.save("blocks.png")
