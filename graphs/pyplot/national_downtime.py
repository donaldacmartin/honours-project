from matplotlib import use
use("Agg")
from matplotlib.pyplot import plot, savefig, xlabel, ylabel, title, clf
from utilities.geoip import GeoIPLookup

class NationalDownTimeChart(object):
    def __init__(self, bgp_dumps, country_iso):
        self.geo = GeoIPLookup("EG")

        dates          = [bgp_dump.datetime for bgp_dump in bgp_dumps]
        vis_blocks     = [bgp.visible_blocks for bgp in bgp_dumps]
        country_blocks = [national(block, country_iso) for block in vis_blocks]
        ip_space       = [total_space(block) for block in country_blocks]

        # num_cxns = [len(bgp_dump.asys_connections) for bgp_dump in bgp_dumps]

        self.draw("Visible IP Address Space", "Visible Addresses", dates, ip_space, "ip_space.png")
        # self.draw("Number of Connections between Autonomous Systems", "Visible Connections", dates, num_cxns, "asys_cxns.png")

    def national(self, blocks, country_iso):
        return [(ip,_) for (ip,_) in blocks if in_country(ip, country_iso)]

    def in_country(self, ip_addr, country_iso):
        return self.geo.get_country_for_ip(ip_addr) == country_iso

    def total_space(self, blocks):
        blocks = [cidr_to_int(i) for (_, i) in blocks]
        return sum(blocks)

    def draw(self, chart_title, axis_name, dates, metric, filename):
        clf()

        title(chart_title)
        ylabel(axis_name)
        xlabel("Date & Time")

        plot(dates, metric)
        savefig(filename)
