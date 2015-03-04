from unittest import TestCase, main
from utilities.file.search import FileBrowser

class TestFileSearch(TestCase):
    def setUp(self):
        base_dir   = "/nas05/users/csp/routing-data/archive.routeviews.org"
        self.files = FileBrowser(base_dir)

    def get_files_for_valid_time(self):
        files_found = self.files.get_files_for_time(2014, 1, 1, 00)
        self.assertTrue(len(files_found) > 0)

    def get_files_for_invalid_year(self):
        self.assertRaises(Exception, self.files.get_files_for_time, (1996, 1, 1, 00))

    def get_files_for_invalid_month(self):
        self.assertRaises(Exception, self.files.get_files_for_time, (2014, 13, 1, 00))

    def get_files_for_invalid_day(self):
        self.assertRaises(Exception, self.files.get_files_for_time, (2014, 1, 32, 00))

    def get_files_for_invalid_hour(self):
        self.assertRaises(Exception, self.files.get_files_for_time, (2014, 1, 1, 24))

    def get_year_end_files(self):
        files_found = self.files.get_year_end_files(2013)
        self.assertTrue(len(files_found) > 0)

if __name__ == "__main__":
    main()
