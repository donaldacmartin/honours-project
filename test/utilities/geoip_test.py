from unittest import TestCase
from utilities.geoip import GeoIPLookup

class TestGeoIP(TestCase):
    def setUp(self):
        self.geoip = GeoIPLookup()

    def test_british_ip(self):
        ip_address = "130.209.34.12"
        country    = self.geoip.get_country_for_ip(ip_address)
        self.assertEqual("GBR", country)

    def test_american_ip(self):
        ip_address = "173.252.148.104"
        country    = self.geoip.get_country_for_ip(ip_address)
        self.assertEqual("USA", country)

    def test_canadian_ip(self):
        ip_address = "205.193.117.158"
        country    = self.geoip.get_country_for_ip(ip_address)
        self.assertEqual("CAN", country)

    def test_invalid_ip(self):
        ip_address = "256.0.0.0"
        self.assertRaises(Exception, self.geoip.get_country_for_ip, ip_address)
