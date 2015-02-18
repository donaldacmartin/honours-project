from re import search

IPV4_RESERVED_SPACE    =  592708864.0
IPV4_ADDRESSABLE_SPACE = 4294967296.0
IPV4_PUBLIC_SPACE      = IPV4_ADDRESSABLE_SPACE - IPV4_RESERVED_SPACE

class AddressBlock(object):
    def __init__(self, base_ip_address, cidr_size):
        self.base_address = base_ip_address
        self.last_address = ip_to_int(base_ip_address) + cidr_to_int(cidr_size)
        self.cidr_size    = cidr_size
        self.int_size     = cidr_to_int(cidr_size)


def parse_ipv4_block(ip_block):
    if search("[a-zA-Z]+", ip_block) is not None or ":" in ip_block:
        raise Exception("IPv6 Address Encountered: " + ip_block)

    if "/" in ip_block:
        ip_address, prefix_size = ip_block.split("/")
        return (ip_address, int(prefix_size))
    else:
        prefix_size = sig_figs_to_cidr(ip_block)
        return (ip_block, prefix_size)

def ip_to_int(ip_address, is_host=False):
    if ":" in ip_address:
        return None

    octets = ip_address.split(".")

    if len(octets) != 4 or not all([0 <= int(o) <= 255 for o in octets]):
        return None

    o1 = int(octets[0]) * 16777216
    o2 = int(octets[1]) * 65536
    o3 = int(octets[2]) * 256
    o4 = int(octets[3]) if not is_host or int(octets[3]) > 0 else 1

    return o1 + o2 + o3 + o4

def int_to_ip(integer):
    if not 0 <= integer <= 4294967295:
        return None

    o1 = int(integer / 16777216) % 256
    o2 = int(integer /    65536) % 256
    o3 = int(integer /      256) % 256
    o4 = int(integer           ) % 256

    octets = [str(o) for o in [o1, o2, o3, o4]]
    return ".".join(octets)

def cidr_to_int(cidr):
    host_size = 32 - int(cidr)
    return 2 ** host_size if 1 <= cidr <= 32 else None

def sig_figs_to_cidr(ip_address):
    octets = [int(octet) for octet in ip_address.split(".")]
    return 32 if 0 not in octets else 8 * octets.index(0)

def get_reserved_blocks():
    return [(ip_to_int("0.0.0.0"),  8),         # RFC 1700
            (ip_to_int("10.0.0.0"), 8),         # RFC 1918
            (ip_to_int("100.64.0.0"), 10),      # RFC 6598
            (ip_to_int("127.0.0.0"), 8),        # RFC  990
            (ip_to_int("169.254.0.0"), 16),     # RFC 3927
            (ip_to_int("172.16.0.0"), 12),      # RFC 1918
            (ip_to_int("192.0.0.0"), 24),       # RFC 5736
            (ip_to_int("192.88.99.0"), 24),     # RFC 3068
            (ip_to_int("192.168.0.0"), 16),     # RFC 1918
            (ip_to_int("198.18.0.0"), 15),      # RFC 2544
            (ip_to_int("198.51.100.0"), 24),    # RFC 5737
            (ip_to_int("203.0.113.0"), 24),     # RFC 5737
            (ip_to_int("224.0.0.0"), 4),        # RFC 5771
            (ip_to_int("240.0.0.0"), 4),        # RFC 6890
            (ip_to_int("255.255.255.255"), 32)  # RFC 6890
            ]
