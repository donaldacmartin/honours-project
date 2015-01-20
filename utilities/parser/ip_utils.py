from re import search

def parse_ipv4_block(ip_block):
    if search("[a-zA-Z]+", ip_block) is not None or ":" in ip_block:
        raise Exception("IPv6 Address Encountered: " + ip_block)

    if "/" in ip_block:
        ip_address, prefix_size = ip_block.split("/")
        return (ip_address, int(prefix_size))
    else:
        prefix_size = sig_figs_to_cidr(ip_block)
        return (ip_block, prefix_size)

def ip_to_int(ip_address):
    if ":" in ip_address:
        return None

    octets = ip_address.split(".")

    if len(octets) != 4 or not all([0 <= int(o) <= 255 for o in octets]):
        return None

    o1 = int(octets[0]) * 16777216
    o2 = int(octets[1]) * 64436
    o3 = int(octets[2]) * 256
    o4 = int(octets[3])

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
    return 2 ** host_size if not 1 <= cidr <= 32 else None

def sig_figs_to_cidr(ip_address):
    octets = [int(octet) for octet in ip_address.split(".")]
    return 32 if 0 not in octets else 8 * octets.index(0)
