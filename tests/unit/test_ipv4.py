"""Unit tests for IPv4 network calculations and validation."""

import ipaddress

import pytest

from yggdevsec_subnetting.ipv4 import (
    get_ip_class,
    parse_ipv4,
    parse_network,
    prefix_for_hosts,
    usable_range,
)


def test_parse_network_normalizes_host_bits():
    network = parse_network("172.16.1.10/22")

    assert network == ipaddress.IPv4Network("172.16.0.0/22")


@pytest.mark.parametrize("value", ["2001:db8::/32", "invalid"])
def test_parse_network_rejects_invalid_ipv4(value):
    with pytest.raises(ValueError):
        parse_network(value)


def test_parse_ipv4():
    address = parse_ipv4("172.16.0.1")

    assert address == ipaddress.IPv4Address("172.16.0.1")


@pytest.mark.parametrize("value", ["2001:db8::1", "invalid"])
def test_parse_ipv4_rejects_invalid_address(value):
    with pytest.raises(ValueError):
        parse_ipv4(value)


@pytest.mark.parametrize(
    ("hosts", "expected_prefix"),
    [
        (1, 30),
        (2, 30),
        (18, 27),
        (40, 26),
        (180, 24),
        (400, 23),
    ],
)
def test_prefix_for_hosts(hosts, expected_prefix):
    assert prefix_for_hosts(hosts) == expected_prefix


@pytest.mark.parametrize("hosts", [0, -1, 2**32])
def test_prefix_for_hosts_rejects_invalid_values(hosts):
    with pytest.raises(ValueError):
        prefix_for_hosts(hosts)


@pytest.mark.parametrize(
    ("cidr", "expected"),
    [
        ("172.16.3.0/26", ("172.16.3.1", "172.16.3.62", 62)),
        ("172.16.3.96/30", ("172.16.3.97", "172.16.3.98", 2)),
        ("192.0.2.0/31", ("192.0.2.0", "192.0.2.1", 2)),
        ("192.0.2.10/32", ("192.0.2.10", "192.0.2.10", 1)),
    ],
)
def test_usable_range(cidr, expected):
    network = ipaddress.IPv4Network(cidr)

    assert usable_range(network) == expected


@pytest.mark.parametrize(
    ("cidr", "expected_class"),
    [
        ("0.0.0.0/8", "Reserved (0/8)"),
        ("10.0.0.0/8", "A"),
        ("126.0.0.0/8", "A"),
        ("127.0.0.0/8", "Loopback (127/8)"),
        ("128.0.0.0/8", "B"),
        ("172.16.0.0/22", "B"),
        ("192.168.1.0/24", "C"),
        ("224.0.0.0/4", "D"),
        ("240.0.0.0/4", "E"),
    ],
)
def test_get_ip_class(cidr, expected_class):
    network = ipaddress.IPv4Network(cidr)

    assert get_ip_class(network) == expected_class
