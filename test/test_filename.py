from unittest import TestCase, main
from utilities.file.name import get_date_for_filename
from datetime import datetime

class TestFilename(TestCase):
    def test_cisco_filename_with_date(self):
        filename = "oix-route-views/1997.11/oix-full-1997-11-08-1724.dat.bz2"
        expected = datetime(1997, 11, 8, 17)
        result   = get_date_for_filename(filename)
        self.assertEqual(expected, result)

    def test_cisco_filename_with_rv3_date(self):
        filename = "route-views3/2007.04/route-views3-full-snapshot-2007-04-20-1600.dat.bz2"
        expected = datetime(2007, 04, 20, 16)
        result   = get_date_for_filename(filename)
        self.assertEqual(expected, result)

    def test_cisco_filename_without_date(self):
        filename = "oix-route-views/1997.11/latest.dat.bz2"
        self.assertRaises(Exception, get_date_for_filename, filename)

    def test_rib_filename(self):
        filename = "bgpdata/2001.10/RIBS/rib.2011026.1648.bz2"
        expected = datetime(2001, 10, 26, 16)
        result   = get_date_for_filename(filename)
        self.assertEqual(expected, result)

    def test_updates_filename(self):
        filename = "route-views3/2014.04/UPDATES/updates.20140408.1045.bz2"
        self.assertRaises(Exception, get_date_for_filename, filename)

    def test_invalid_filename(self):
        filename = "invalid_filename"
        self.assertRaises(Exception, get_date_for_filename, filename)

if __name__ == "__main__":
    main()
