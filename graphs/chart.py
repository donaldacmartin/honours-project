#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from matplotlib import use
use("Agg")
from matplotlib.pyplot import plot, savefig, xlabel, ylabel, title, clf

"""
Chart

Given one or more BGP dump files, draw a number of charts. These are stored as
one object, as PyPlot creates a plot as a global variable, meaing that more than
one cannot be in the interpreter at the same time.
"""

IPV4_RESERVED_SPACE    =  592708864.0
IPV4_ADDRESSABLE_SPACE = 4294967296.0
IPV4_PUBLIC_SPACE      = IPV4_ADDRESSABLE_SPACE - IPV4_RESERVED_SPACE

class Chart(object):
    def __init__(self, bgp_dumps):
        self.bgp_dumps = bgp_dumps

    def _plot_yearly_data(self, statistic, filename):
        yearly_data = _get_yearly_data(statistic, self.bgp_dumps)

        x_values = [data[0] for data in yearly_data]
        y_values = [data[1] for data in yearly_data]

        xlabel("Year")
        plot(x_values, y_values)
        savefig(filename)

    def draw_yearly_address_space(self, filename):
        clf()
        ylabel("IPv4 Address Space Usage")
        title("Yearly IPv4 Address Space Usage")
        self._plot_yearly_data(_visible_address_space, filename)

    def draw_yearly_mode_allocated_block_size(self, filename):
        clf()
        ylabel("Block Size")
        title("Yearly Most Commonly Allocated Block Size")
        self._plot_yearly_data(_mode_block_size, filename)

    def draw_yearly_mean_allocated_block_size(self, filename):
        clf()
        ylabel("Block Size")
        title("Yearly Mean Allocated Block Size")
        self._plot_yearly_data(_mean_block_size, filename)

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
    return (dump.visible_address_space / IPV4_PUBLIC_SPACE) * 100

def _mode_block_size(dump):
    return dump.alloc_blocks.index(max(dump.alloc_blocks)) + 1

def _mean_block_size(dump):
    blocks = dump.alloc_blocks
    total  = 0

    for i in range(32):
        total += blocks[i] * (i+1)

    return int(total / 32)
