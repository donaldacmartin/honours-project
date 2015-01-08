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

        self.oix_dumps = {}
        self.rib_dumps = {}

        self._organise_into_dates(files)

    def _load_all_files(self, directory):
        files  = []

        for file_data in walk(directory):
            path      = file_data[0]
            filenames = file_data[2]
            dir_files = [path + "/" + filename for filename in filenames]
            files     += dir_files

        return files

    def _filter_files(self, files):
        return [file for file in files if file.endswith(".bz2")]

    def _organise_into_dates(self, files):
        for filename in files:
            if "oix" in filename:
                self._map_oix_filename(filename)
            elif "RIBS" in filename:
                self._map_rib_filename(filename)

    def _map_oix_filename(self, filename):
        tokens = filename.split("-")

        yy = int(tokens[-4])
        mm = int(tokens[-3])
        dd = int(tokens[-2])
        hh = int(tokens[-1].split(".")[0][0:2])

        self.oix_dumps[(yy, mm, dd, hh)] = filename

    def _map_rib_filename(self, filename):
        tokens = filename.split(".")

        yy = int(tokens[-3][0:4])
        mm = int(tokens[-3][4:6])
        dd = int(tokens[-3][6:8])
        hh = int(tokens[-2][0:2])

        self.rib_dumps[(yy, mm, dd, hh)] = filename
