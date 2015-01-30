#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from matplotlib import use
use("Agg")
from matplotlib.pyplot import plot, savefig, xlabel, ylabel, ylim, title, clf
from collections import Counter
from utilities.parser.ip_utils import IPV4_PUBLIC_SPACE

"""
Chart

Given one or more BGP dump files, draw a number of charts. These are stored as
one object, as PyPlot creates a plot as a global variable, meaing that more than
one cannot be in the interpreter at the same time.
"""

class YearlyChart(object):
    def __init__(self, bgp_dumps):
        self.bgp_dumps = bgp_dumps

    def _plot_yearly_data(self, statistic):
        yearly_data = _get_yearly_data(statistic, self.bgp_dumps)

        x_values = [data[0] for data in yearly_data]
        y_values = [data[1] for data in yearly_data]

        xlabel("Year")
        plot(x_values, y_values)

    def draw_address_space(self, filename):
        clf()
        ylabel("% IPv4 Space")
        title("Yearly % IPv4 Space Visible to Routers")
        self._plot_yearly_data(_visible_address_space)
        ylim(0, 100)
        savefig(filename)

    def draw_most_common_block_size(self, filename):
        clf()
        ylabel("Prefix Size")
        title("Yearly Most Commonly Allocated Prefix Size")
        self._plot_yearly_data(_most_common_block_size)
        ylim(0,32)
        savefig(filename)

# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------

def _get_yearly_data(statistic, dumps):
    yearly_data = []

    for dump in dumps:
        year = dump.date_time_stamp[0]
        data = statistic(dump)
        yearly_data.append((year, data))

    return yearly_data

def _visible_address_space(dump):
    return (dump.get_visible_space_size() / IPV4_PUBLIC_SPACE) * 100

def _most_common_block_size(dump):
    counter = Counter()

    for (_, cidr) in dump.visible_blocks:
        counter[cidr] += 1

    return counter.most_common(1)[0][0]
