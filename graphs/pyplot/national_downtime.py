from matplotlib import use
use("Agg")
from matplotlib.pyplot import plot, savefig, xlabel, ylabel, title, clf

class NationalDownTimeChart(object):
    def __init__(self, bgp_dumps):
        dates = [bgp_dump.datetime for bgp_dump in bgp_dumps]

        ip_space = [bgp_dump.get_visible_space_size() for bgp_dump in bgp_dumps]
        num_cxns = [len(bgp_dump.asys_connections) for bgp_dump in bgp_dumps]

        self.draw("Visible IP Address Space", "Visible Addresses", dates, ip_space, "ip_space.png")
        self.draw("Number of Connections between Autonomous Systems", "Visible Connections", dates, num_cxns, "asys_cxns.png")

    def draw(self, chart_title, axis_name, dates, metric, filename):
        clf()

        title(chart_title)
        ylabel(axis_name)
        xlabel("Date & Time")

        plot(dates, metric)
        savefig(filename)
