#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from unittest import TestCase
from utilities.parser.ip_utils import *

class IPUtilsTest(TestCase):
    # --------------------------------------------------------------------------
    # IP to Integer Conversion
    # --------------------------------------------------------------------------
    def test_ip_to_int_lower_limit(self):
        integer = ip_to_int("0.0.0.0")
        self.assertEqual(0, integer, "Lower IPv4 limit failed")

    def test_ip_to_int_upper_limit(self):
        integer = ip_to_int("255.255.255.255")
        self.assertEqual(4294967295, integer, "Upper IPv4 limit failed")

    def test_ip_to_int_negative(self):
        integer = ip_to_int("0.0.0.-1")
        self.assertEqual(None, integer, "Negative IP address did not fail")

    def test_ip_to_int_exceeding_limit(self):
        integer = ip_to_int("255.255.255.256")
        self.assertEqual(None, integer, "Too large IP address did not fail")

    def test_ip_to_int_ipv6(self):
        integer = ip_to_int("ff01::1")
        self.assertEqual(None, integer, "IPv6 address did not fail")

    # --------------------------------------------------------------------------
    # Integer to IP Conversion
    # --------------------------------------------------------------------------
    def test_int_to_ip_lower_limit(self):
        ip = int_to_ip(0)
        self.assertEqual("0.0.0.0", ip, "Lower IPv4 limit failed")

    def test_int_to_ip_upper_limit(self):
        ip = int_to_ip(4294967295)
        self.assertEqual("255.255.255.255", ip, "Upper IPv4 limit failed")

    def test_int_to_ip_negative(self):
        ip = int_to_ip(-1)
        self.assertEqual(None, ip, "Negative integer did not fail")

    def test_int_to_ip_exceeding_limit(self):
        ip = int_to_ip(4294967296)
        self.assertEqual(None, ip, "Too large integer did not fail")

    # --------------------------------------------------------------------------
    # Converting CIDR to Integers
    # --------------------------------------------------------------------------
    def test_cidr_to_int


    def test_parse_ipv4_block_with_cidr(self):
        pass

    def test_parse_ipv4_block_without_cidr(self):
        pass

    def test_rejection_of_ipv6(self):
        pass
