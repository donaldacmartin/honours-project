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
        self.assertEqual(None, ip, "Integer larger than possible did not fail")

    # --------------------------------------------------------------------------
    # Converting CIDR to Integers
    # --------------------------------------------------------------------------
    def test_cidr_to_int_lower_limit(self):
        size = cidr_to_int(1)
        self.assertEqual(0, size, "Largest prefix failed")

    def test_cidr_to_int_upper_limit(self):
        size = cidr_to_int(32)
        self.assertEqual(1, size, "Smallest prefix failed")

    def test_cidr_to_int_negative(self):
        size = cidr_to_int(-1)
        self.assertEqual(None, size, "Negative CIDR did not fail")

    def test_cidr_to_int_exceeding_limit(self):
        size = cidr_to_int(33)
        self.assertEqual(None, size, "CIDR larger than possible did not fail")

    # --------------------------------------------------------------------------
    # Converting Significant Figures to CIDR (Cisco notation)
    # --------------------------------------------------------------------------
    def sig_figs_to_cidr_lower_limit(self):
        cidr = sig_figs_to_cidr("0.0.0.0")
        self.assertEqual(8, cidr, "Minimum prefix size failed")

    def sig_figs_to_cidr_upper_limit(self):
        cidr = sig_figs_to_cidr("255.255.255.255")
        self.assertEqual(32, cidr, "Maximum prefix size failed")

    # --------------------------------------------------------------------------
    # Overall Parsing
    # --------------------------------------------------------------------------
    def test_parse_ipv4_block_with_cidr(self):
        ip_addr, cidr = parse_ipv4_block("0.0.0.0/8")
        self.assertEqual("0.0.0.0", ip_addr, "Wrong IP address returned")
        self.assertEqual(8, cidr, "Wrong CIDR prefix size returned")

    def test_parse_ipv4_block_without_cidr(self):
        ip_addr, cidr = parse_ipv4_block("0.0.0.0")
        self.assertEqual("0.0.0.0", ip_addr, "Wrong IP address returned")
        self.assertEqual(8, cidr, "Wrong CIDR prefix size returned")

    def test_rejection_of_ipv6(self):
        self.assertRaises(Exception, parse_ipv4_block, "ff01::1")
