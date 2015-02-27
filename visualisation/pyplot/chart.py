#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from matplotlib import use
use("Agg")
from matplotlib.pyplot import plot, savefig, xlabel, ylabel, ylim, title, clf, subplots, legend, figure
from collections import Counter
from numpy import array
from parser.ip_utils import IPV4_PUBLIC_SPACE

"""
Chart

Given one or more BGP dump files, draw a number of charts. These are stored as
one object, as PyPlot creates a plot as a global variable, meaing that more than
one cannot be in the interpreter at the same time.
"""

class YearlyChart(object):
    def __init__(self, bgp_dumps, width, height):
        # width  = width / 300
        # height = height / 300

        # figure(figsize=(width, height), dpi=300)
        self.bgp_dumps = bgp_dumps
        self.years     = [bgp_dump.datetime.year for bgp_dump in bgp_dumps]

    def plot_yearly_data(self, metric, chart_title, y_axis_label, lim1, lim2):
        clf()
        title(chart_title)
        y_values = [metric(bgp_dump) for bgp_dump in self.bgp_dumps]
        ylabel(y_axis_label)
        xlabel("Year")
        ylim(lim1, lim2)
        plot(self.years, y_values)

    def draw_address_space(self, filename):
        chart = "Yearly % IPv4 Space Visible to Routers"
        label = "% IPv4 Space"
        self.plot_yearly_data(visible_address_space, chart, label, 0, 100)
        savefig(filename)

    def draw_most_common_block_size(self, filename):
        chart = "Yearly Most Commonly Allocated Prefix Size"
        label = "Prefix Size"
        self.plot_yearly_data(most_common_block_size, chart, label, 0, 32)
        savefig(filename)

    def draw_stacked_allocation_of_blocks(self, filename):
        clf()
        all_totals  = [[] for _ in range(32)]
        last_totals = [0 for _ in range(32)]

        for bgp_dump in self.bgp_dumps:
            bgp_totals = bgp_dump.get_block_size_totals()

            i = 0

            while i < 32:
                all_totals[i].append(bgp_totals[i] - last_totals[i])
                i += 1

            last_totals = bgp_totals

        all_totals = [array(total) for total in all_totals]
        fig, ax = subplots()
        ax.stackplot(self.years, *all_totals)
        savefig(filename)

# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------

def visible_address_space(dump):
    return (dump.get_visible_space_size() / IPV4_PUBLIC_SPACE) * 100

def most_common_block_size(dump):
    counter = Counter()

    for (_, cidr) in dump.visible_blocks:
        counter[cidr] += 1

    return counter.most_common(1)[0][0]
