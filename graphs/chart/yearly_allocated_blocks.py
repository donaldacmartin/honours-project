from __future__ import division
from base import BaseChart
from utilities.parser.ip_utils import ip_to_int, cidr_to_int

DEFAULT = ("0.0.0.0", "255.255.255.255")
TESTING = ("4.0.0.0", "4.255.255.255")

class YearlyAllocatedBlocks(BaseChart):
    def __init__(self, bgp_dumps, bounds=DEFAULT, width=1920, height=1080):
        super(YearlyAllocatedBlocks, self).__init__(width, height)

        self.base     = ip_to_int(bounds[0])
        self.limit    = ip_to_int(bounds[1])
        self.ip_range = self.limit / self.base
        row_delta     = self.image.size[1] / len(bgp_dumps)
        row_pos       = self.image.size[1] * 0.1

        for bgp_dump in bgp_dumps:
            blocks = bgp_dump.visible_blocks
            blocks = [(ip, cidr) for (ip,cidr) in blocks if base <= ip <= limit]
            self.draw_row(blocks, row_pos)
            row_pos += row_delta

    def draw_row(self, blocks, row_pos):
        for (ip, cidr) in blocks:
            start = self.ip_to_x_coord(ip)
            end   = self.ip_to_x_coord(ip + cidr_to_int(cidr))
            self.draw_line((start, row_pos), (end, row_pos))

    def ip_to_x_coord(self, ip):
        return (ip - self.base) * self.ip_range
