#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from matplotlib import use
use("Agg")
from matplotlib.pyplot import plot, savefig

def create_yearly_address_space(bgp_dumps):
    yearly_data = _organise_dumps_into_yearly_data(bgp_dumps)

    x_values = [data[0] for data in yearly_data]
    y_values = [data[1] for data in yearly_data]

    plot(x_values, y_values)
    savefig("yearly-address-space.png")

def _organise_dumps_into_yearly_data(dumps):
    yearly_data = []

    for dump in dumps:
        year  = dump.date_time_stamp[0]
        space = dump.visible_address_space / 4 294 967 296.0
        yearly_data.append((year, space))

    return yearly_data
