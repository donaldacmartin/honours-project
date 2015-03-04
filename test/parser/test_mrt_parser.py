from unittest import TestCase, main
from parser.mrt import MRTParser
from parser.exception import *

"""
MRT Parser Test

Tests the parser that accepts files in MRT binary format. As it is hard to
generate MRT binary files for bgpdump to recognise, the parser is being
initialised with "None" so that the parse_line function can be called directly,
allowing us to check the effect of the action instantly.

As bgpdump is a third-party tool, it can be assumed that this software is
operating correctly, as parsing of binary data is outside the scope of this
project.

The following line is being used as a basis for testing:

TABLE_DUMP|1004488339|B|4.0.0.2|1|3.0.0.0/8|
1 701 80|IGP|4.0.0.2|0|21040|1:666|NAG||

"""

class TestMRTParser(TestCase):
    def setUp(self):
        self.parser       = MRTParser(None)
        self.correct_line = ("TABLE_DUMP|1004488339|B|4.0.0.2|1|3.0.0.0/8|"
                             "1 701 80|IGP|4.0.0.2|0|21040|1:666|NAG||")

    def test_correct_path(self):
        self.parser.parse_line(self.correct_line)

        expected_connections = set([(1, 701), (80, 701)])
        parsed_connections   = self.parser.asys_connections
        self.assertEqual(expected_connections, parsed_connections)

    def test_correct_ip_prefix(self):
        self.parser.parse_line(self.correct_line)

        parsed_ip_addrs   = self.parser.asys_to_ip_addr[80]
        expected_ip_addr  = "3.0.0.0"

        self.assertTrue(expected_ip_addr in parsed_ip_addrs)

    def test_correct_num_connections(self):
        self.parser.parse_line(self.correct_line)

        total_parsed_connections   = len(self.parser.asys_connections)
        total_expected_connections = 2

        self.assertEqual(total_expected_connections, total_parsed_connections)

    def test_correct_asys_size(self):
        self.parser.parse_line(self.correct_line)

        parsed_asys_size   = self.parser.asys_size[80]
        expected_asys_size = 16777216

        self.assertEqual(expected_asys_size, parsed_asys_size)

    def test_incorrect_number_tokens(self):
        line = ("TABLE_DUMP|1004488339|B|4.0.0.2|0|21040|1:666|NAG||")
        self.assertRaises(Exception, self.parser.parse_line, line)

    def test_tokens_wrong_order(self):
        line = ("TABLE_DUMP|1004488339|B|4.0.0.2|1|IGP|1 701 80|3.0.0.0/8|"
                "4.0.0.2|0|21040|1:666|NAG||")
        self.assertRaises(Exception, self.parser.parse_line, line)

    def test_incorrect_prefix(self):
        line = ("TABLE_DUMP|1004488339|B|4.0.0.2|1|x.x.x.x/x|1 701 80|IGP|"
                "4.0.0.2|0|21040|1:666|NAG||")
        self.assertRaises(InvalidIPAddressError, self.parser.parse_line, line)

    def test_ipv6_prefix(self):
        line = ("TABLE_DUMP|1004488339|B|4.0.0.2|1|f::::0/8|1 701 80|IGP|"
                "4.0.0.2|0|21040|1:666|NAG||")
        self.assertRaises(InvalidIPAddressError, self.parser.parse_line, line)

    def test_repeated_asys_on_path(self):
        line = ("TABLE_DUMP|1004488339|B|4.0.0.2|1|3.0.0.0/8|1 701 701 80|IGP|"
                "4.0.0.2|0|21040|1:666|NAG||")
        self.parser.parse_line(line)

        expected_connections = set([(1, 701), (80, 701)])
        parsed_connections   = self.parser.asys_connections

        self.assertEqual(expected_connections, parsed_connection)

    def test_path_incomplete(self):
        line = ("TABLE_DUMP|1004488339|B|4.0.0.2|1|3.0.0.0/8|1 701 ?|IGP|"
                "4.0.0.2|0|21040|1:666|NAG||")
        self.parser.parse_line(line)

        total_parsed_connections   = len(self.parser.asys_connections)
        total_expected_connections = 1

        self.assertEqual(total_expected_connections, total_parsed_connections)

if __name__ == "__main__":
    main()
