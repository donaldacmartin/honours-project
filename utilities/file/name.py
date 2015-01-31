#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from datetime import datetime

"""
FileName

A method used to translate a filename into a tuple containing a timestamp in the
format (YY, MM, DD, HH). Minutes are not recorded as the vast majority of dumps
were taken exactly on the hour, making this measurement irrelevant for most
useful comparisons.
"""

def get_date_for_filename(name):
    if "UPDATES" in name:
        raise Exception("Updates file detected")
    elif "oix" in name or ("route-views3" in name and "RIBS" not in name):
        return translate_cisco_filename(name)
    else:
        return translate_ribs_filename(name)

def translate_cisco_filename(filename):
    try:
        if "latest.dat.bz2" in filename:
            raise Exception("Unable to parse Cisco style filename: " + filename)

        tokens = filename.split("-")

        yy = int(tokens[-4])
        mm = int(tokens[-3])
        dd = int(tokens[-2])
        hh = int(tokens[-1].split(".")[0][0:2])

        return datetime(yy, mm, dd, hh)
    except:
        raise Exception("Unable to parse Cisco style filename: " + filename)

def translate_ribs_filename(filename):
    try:
        tokens = filename.split(".")

        yy = int(tokens[-3][0:4])
        mm = int(tokens[-3][4:6])
        dd = int(tokens[-3][6:8])
        hh = int(tokens[-2][0:2])

        return datetime(yy, mm, dd, hh)
    except:
        raise Exception("Unable to parse RIBS style filename: " + filename)
