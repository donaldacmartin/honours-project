#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from unittest import TestCase, main
from parser.ip_utils import *
from parser.exception import *

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
        self.assertRaises(InvalidIPAddressError, ip_to_int, "0.0.0.-1")

    def test_ip_to_int_exceeding_limit(self):
        self.assertRaises(InvalidIPAddressError, ip_to_int, "255.255.255.256")

    def test_ip_to_int_ipv6(self):
        self.assertRaises(InvalidIPAddressError, ip_to_int, "ff01::1")

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
        self.assertRaises(InvalidIPAddressError, int_to_ip, -1)

    def test_int_to_ip_exceeding_limit(self):
        self.assertRaises(InvalidIPAddressError, int_to_ip, 4294967296)

    # --------------------------------------------------------------------------
    # Converting CIDR to Integers
    # --------------------------------------------------------------------------
    def test_cidr_to_int_lower_limit(self):
        size = cidr_to_int(1)
        self.assertEqual(2147483648, size, "Smallest prefix failed")

    def test_cidr_to_int_upper_limit(self):
        size = cidr_to_int(32)
        self.assertEqual(1, size, "Largest prefix failed")

    def test_cidr_to_int_negative(self):
        self.assertRaises(CIDRError, cidr_to_int, -1)

    def test_cidr_to_int_exceeding_limit(self):
        self.assertRaises(CIDRError, cidr_to_int, 33)

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
        ip_addr, cidr = parse_ipv4_block("1.0.0.0/8")
        self.assertEqual("1.0.0.0", ip_addr, "Wrong IP address returned")
        self.assertEqual(8, cidr, "Wrong CIDR prefix size returned")

    def test_parse_ipv4_block_without_cidr(self):
        ip_addr, cidr = parse_ipv4_block("1.0.0.0")
        self.assertEqual("1.0.0.0", ip_addr, "Wrong IP address returned")
        self.assertEqual(8, cidr, "Wrong CIDR prefix size returned")

    def test_rejection_of_ipv6(self):
        self.assertRaises(Exception, parse_ipv4_block, "ff01::1")

if __name__ == "__main__":
    main()
