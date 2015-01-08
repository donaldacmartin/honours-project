#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from os import walk

"""
FileBrowser

An object that parses a directory for routing dumps and can present them in
"""

class FileBrowser(object):
    def __init__(self, directory):
        self.oix_dumps  = {}
        self.eqix_dumps = {}
        self.isc_dumps  = {}
        self.rv1_dumps  = {}
        self.rv3_dumps  = {}
        self.rv4_dumps  = {}

        self.all_routers = (self.oix_dumps,
                            self.eqix_dumps,
                            self.isc_dumps,
                            self.rv1_dumps,
                            self.rv3_dumps,
                            self.rv4_dumps)

        files = self._load_all_files(directory)
        files = self._filter_files(files)
        self._organise_into_dates(files)

    def get_files_for_time(self, yy, mm, dd, hh):
        files = []

        for router in self.all_routers:
            dump = self._try_to_find_dump(router, yy, mm, dd, hh)

            if dump is not None:
                files.append(dump)

        return files

    def get_available_timestamps(self):
        keys = set()

        for router in self.all_routers:
            router_keys = router.keys()

            for k in router_keys:
                keys.add(k)

        return sorted(keys)

    def _try_to_find_dump(self, router, yy, mm, dd, hh):
        if (yy, mm, dd, hh) in router:
            return router[(yy, mm, dd, hh)]

        if (yy, mm, dd, hh-1) in router:
            return router[(yy, mm, dd, hh-1)]

        if (yy, mm, dd, hh+1) in router:
            return router[(yy, mm, dd, hh+1)]

        return None

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
            if "UPDATES" in filename:
                continue

            if "oix" in filename:
                self._map_cisco_filename(filename, self.oix_dumps)
            elif "eqix" in filename:
                self._map_ribs_filename(filename, self.eqix_dumps)
            elif "isc" in filename:
                self._map_ribs_filename(filename, self.isc_dumps)
            elif "route-views3" in filename and "RIBS" in filename:
                self._map_ribs_filename(filename, self.rv3_dumps)
            elif "route-views3" in filename and "RIBS" not in filename:
                self._map_cisco_filename(filename, self.rv3_dumps)
            elif "route-views4" in filename:
                self._map_ribs_filename(filename, self.rv4_dumps)
            elif "RIBS" in filename:
                self._map_ribs_filename(filename, self.rv1_dumps)
            else:
                print("Unable to classify filename: " + filename)

    def _map_cisco_filename(self, filename, dump_location):
        try:
            if "latest.dat.bz2" in filename:
                return

            tokens = filename.split("-")

            yy = int(tokens[-4])
            mm = int(tokens[-3])
            dd = int(tokens[-2])
            hh = int(tokens[-1].split(".")[0][0:2])

            dump_location[(yy, mm, dd, hh)] = filename
        except:
            print("Unable to parse Cisco style filename: " + filename)

    def _map_ribs_filename(self, filename, dump_location):
        try:
            tokens = filename.split(".")

            yy = int(tokens[-3][0:4])
            mm = int(tokens[-3][4:6])
            dd = int(tokens[-3][6:8])
            hh = int(tokens[-2][0:2])

            dump_location[(yy, mm, dd, hh)] = filename
        except:
            print("Unable to parse RIBS style filename: " + filename)
