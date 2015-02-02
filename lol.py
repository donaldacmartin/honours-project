from utilities.parser.mrt import MRTParser
from graphs.pyplot.national_downtime import NationalDownTimeChart

base_dir = "/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/2011.01/RIBS/"
files = ["rib.20110127.2000.bz2",
         "rib.20110127.2200.bz2",
         "rib.20110128.0000.bz2",
         "rib.20110128.0200.bz2",
         "rib.20110128.0400.bz2",
         "rib.20110128.0600.bz2",
         "rib.20110128.0800.bz2",
         "rib.20110128.1000.bz2",
         "rib.20110128.1200.bz2",
         "rib.20110128.1400.bz2",
         "rib.20110128.1600.bz2",
         "rib.20110128.1800.bz2",
         "rib.20110128.2000.bz2",
         "rib.20110128.2200.bz2",]

parsers = [MRTParser(base_dir + file) for file in files]
n = NationalDownTimeChart(parsers, "EGY")
