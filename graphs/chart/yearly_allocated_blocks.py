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

        base      = ip_to_int(bounds[0])
        limit     = ip_to_int(bounds[1])
        ip_range  = limit - base

        row_delta = (0.8 * self.image.size[1]) / len(bgp_dumps)
        row_pos   = self.image.size[1] * 0.1

        for bgp_dump in bgp_dumps:
            blocks = bgp_dump.visible_blocks
            blocks = [(ip, cidr) for (ip,cidr) in blocks if base <= ip <= limit]

            for (ip, cidr) in blocks:
                start = self.c(ip, base, ip_range)
                end   = self.c(ip + cidr_to_int(cidr), base, ip_range)
                self.draw_line((start, row_pos), (end, row_pos), width=100)

            row_pos += row_delta

    def c(self, ip, base, ip_range):
        pos = ((ip - base) / ip_range) * (self.image.size[0] * 0.8)
        return pos + (self.image.size[0] * 0.1)

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

    for year in range(2001, 2002):
        years.append(database.get_year_end_files(year))

    years   = [year for year in years if year is not None]
    parsers = [MRTParser(filename[0]) if "rib" in filename[0] else CiscoParser(filename[0]) for filename in years]

    y = YearlyAllocatedBlocks(parsers)
    y.save("tried.png")
