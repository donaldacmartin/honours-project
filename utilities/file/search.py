#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from os import walk
from utilities.file.name import get_date_for_filename

"""
FileBrowser

An object that parses a directory for router dumps and presents them in
dictionaries for each router. Where possible, the router locations have been
specified in the comments below:

- OIX                   Unknown     Unknown     Unknown
- ISC                   Ashburn     Virginia    USA
- ISC                   Palo Alto   California  USA
- RV1, RV3 & RV4        Eugene      Oregon      USA
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
        files = [file for file in files if file.endswith(".bz2")]
        self._organise_into_dates(files)

    def get_files_for_time(self, yy, mm, dd, hh):
        files = []

        for router in self.all_routers:
            dump = self._try_to_find_dump(router, yy, mm, dd, hh)

            if dump is not None:
                files.append(dump)

            if len(files) == 1:
                break

        return files

    def get_year_end_files(self, year):
        for date in range(32, 0, -1):
            for hour in range(24, -1, -1):
                f = self.get_files_for_time(year, 12, date, hour)

                if len(f) > 0:
                    return f

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

    def _organise_into_dates(self, files):
        for filename in files:
            try:
                date_stamp = get_date_for_filename(filename)
            except:
                continue

            if "oix" in filename:
                self.oix_dumps[date_stamp] = filename
            elif "eqix" in filename:
                self.eqix_dumps[date_stamp] = filename
            elif "isc" in filename:
                self.isc_dumps[date_stamp] = filename
            elif "route-views3" in filename:
                self.rv3_dumps[date_stamp] = filename
            elif "route-views4" in filename:
                self.rv4_dumps[date_stamp] = filename
            elif "RIBS" in filename:
                self.rv1_dumps[date_stamp] = filename
            else:
                print("Unable to classify filename: " + filename)
