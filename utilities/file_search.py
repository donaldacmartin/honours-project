#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from os import walk
from re import compile

"""
File Search

Returns a list of paths to BGP binary files in a specified directory. BGP files
are identified by the filename format rib.YYMMDD.HHMM.bz2. Paths are returned
as a list of strings.
"""

class FileBrowser(object):
    def __init__(self, directory):
        files = self._load_all_files(directory)
        files = self._filter_files(files)

        self.database = self._organise_into_dates(files)

    def _load_all_files(self, directory):
        files  = []

        for file_data in walk(directory):
            path      = file_data[0]
            filenames = file_data[2]
            dir_files = [path + "/" + filename for filename in filenames]
            files     += dir_files

        return files

    def _filter_files(self, files):
        return [file for file in files if f.endswith(".bz2")]

    def _organise_into_dates(self, files):
        chrono_listing = {}

        for filename in files:
            yy, mm, dd, hh = self._organise_file(filename)

            if yy is None:
                continue

            if (yy, mm, dd, hh) not in chrono_listing:
                chrono_listing[(yy, mm, dd, hh)] = set()

            chrono_listing[(yy, mm, dd, hh)].add(filename)

        return chrono_listing

    def _organise_file(self, filename):
        if "oix" in filename:
            return self._map_oix_filename(filename)
        elif "RIBS" in filename:
            return self._map_routeviews_filename(filename)

        return (None, None, None, None)

    def _map_oix_filename(self, filename):
        tokens = filename.split("-")

        year  = int(tokens[-4])
        month = int(tokens[-3])
        date  = int(tokens[-2])
        hour  = int(tokens[-1].split(".")[0][0:2])

        return year, month, date, hour

    def _map_routeviews_filename(self, filename):
        tokens = filename.split(".")

        year  = int(tokens[-3][0:4])
        month = int(tokens[-3][4:6])
        date  = int(tokens[-3][6:8])
        hour  = int(tokens[-2][0:2])

        return year, month, date, hour
