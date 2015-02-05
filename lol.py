from utilities.parser.mrt import MRTParser
from graphs.pyplot.national_downtime import NationalDownTimeChart

base_dir = "/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/2011.02/RIBS/"
files = ["rib.20110218.2000.bz2",
         "rib.20110218.2200.bz2",
         "rib.20110219.0000.bz2",
         "rib.20110219.0200.bz2",
         "rib.20110219.0400.bz2"]

parsers = [MRTParser(base_dir + file) for file in files]
n = NationalDownTimeChart(parsers, "LBY")
