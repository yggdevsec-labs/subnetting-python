"""IPv4 network validation and subnet calculations."""

import ipaddress


def parse_network(value: str) -> ipaddress.IPv4Network:
    """Accept an IPv4 CIDR, normalizing host bits to the network address."""
    network = ipaddress.ip_network(value, strict=False)

    if not isinstance(network, ipaddress.IPv4Network):
        raise ValueError("Only IPv4 networks are supported.")

    return network


def parse_ipv4(value: str) -> ipaddress.IPv4Address:
    """Validate and return an IPv4 address."""
    address = ipaddress.ip_address(value)

    if not isinstance(address, ipaddress.IPv4Address):
        raise ValueError("Only IPv4 addresses are supported.")

    return address


def prefix_for_hosts(hosts: int) -> int:
    """Calculate the smallest traditional IPv4 subnet for N hosts."""
    if hosts < 1:
        raise ValueError("Host count must be at least 1.")

    required = hosts + 2

    if required > 2**32:
        raise ValueError("Host count is too large for IPv4.")

    # Reserve network and broadcast addresses; /30 minimum.
    host_bits = max(2, (required - 1).bit_length())

    return 32 - host_bits


def usable_range(network: ipaddress.IPv4Network) -> tuple[str, str, int]:
    """Return usable address range, including RFC 3021 handling."""
    if network.prefixlen >= 31:
        return (
            str(network.network_address),
            str(network.broadcast_address),
            network.num_addresses,
        )

    return (
        str(network.network_address + 1),
        str(network.broadcast_address - 1),
        network.num_addresses - 2,
    )


def get_ip_class(network: ipaddress.IPv4Network) -> str:
    """Return the historical IPv4 address class."""
    first_octet = network.network_address.packed[0]

    if first_octet == 0:
        return "Reserved (0/8)"
    if first_octet == 127:
        return "Loopback (127/8)"
    if first_octet < 128:
        return "A"
    if first_octet < 192:
        return "B"
    if first_octet < 224:
        return "C"
    if first_octet < 240:
        return "D"

    return "E"
