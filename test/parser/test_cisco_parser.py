from unittest import TestCase, main
from parser.cisco import CiscoParser
from parser.exception import *

"""


*> 4.0.0.0          134.24.127.3                           0 1740 1 i
"""

class TestCiscoParser(TestCase):
    def setUp(self):
        self.parser       = CiscoParser(None)
        self.correct_line = ("*> 4.0.0.0          134.24.127.3                "
                             "          0 1740 1 i")

    def test_correct_path(self):
        self.parser.parse_line(self.correct_line)

        expected_paths = set([(1, 1740)])
        parsed_paths   = self.parser.asys_connections

        self.assertEqual(expected_paths, parsed_paths)

    def test_correct_ip_prefix(self):
        self.parser.parse_line(self.correct_line)

        expected_ip_addr = "4.0.0.0"
        parsed_ip_addrs  = self.parser.asys_to_ip_addr[1]

        self.assertTrue(expected_ip_addr in parsed_ip_addrs)

    def test_correct_asys_size(self):
        self.parser.parse_line(self.correct_line)

        expected_size = 16777216
        parsed_size   = self.parser.asys_size[1]

        self.assertEqual(expected_size, parsed_size)

    def test_repeated_asys(self):
        line = "*> 4.0.0.0    134.24.127.3    0 1740 1740 1 i"
        self.parser.parse_line(line)

        expected_connections = set([(1,1740)])
        parsed_connections   = self.parser.asys_connections
        print(parsed_connections)

        self.assertEqual(expected_connections, parsed_connections)

    def test_suppressed_route(self):
        line = "s 4.0.0.0    134.24.127.3    0 1740 1 i"
        self.parser.parse_line(line)

        expected_number_connections = 0
        parsed_number_connections   = len(self.parser.asys_connections)

        self.assertEqual(parsed_number_connections, expected_number_connections)

    def test_incomplete_path(self):
        line = "*> 4.0.0.0    134.24.127.3    0 1740 1 ? i"

        expected_connections = set([(1, 1740)])
        parsed_connections   = self.parser.asys_connections

        self.assertEqual(expected_connections, parsed_connections)

    def test_incorrect_prefix(self):
        line = "*> x.x.x.x    134.24.127.3    0 1740 1 ? i"
        self.assertRaises(InvalidIPAddressError, self.parser.parse_line, line)

if __name__ == "__main__":
    main()
