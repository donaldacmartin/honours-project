import unittest
from utilities.geoip import GeoIPLookup

class GeoIPTest(unittest.TestCase):
    def setUp(self):
        self.geoip = GeoIPLookup()

        self.BBC_IP    = "212.58.246.104"
        self.UNUSED_IP = "0.0.0.0"

    def test_latlon_for_existing_ip(self):
        answer = self.geoip.get_latlon_for_ip(self.BBC_IP)
        latlon = (51.5, -0.13)
        self.assertEqual(answer, latlon, "Wrong latlon coordinates for BBC IP")

    def test_latlon_for_nonexisting_ip(self):
        ip_addr  = self.UNUSED_IP
        function = self.geoip.get_latlon_for_ip
        self.assertRaises(NameError, function, ip_addr)

    def test_country_for_existing_ip(self):
        answer  = self.geoip.get_country_for_ip(self.BBC_IP)
        country = "GB"
        self.assertEqual(answer, country, "Wrong country for BBC IP")

    def test_country_for_nonexisting_ip(self):
        ip_addr  = self.UNUSED_IP
        function = self.geoip.get_country_for_ip
        self.assertRaises(NameError, function, ip_addr)
