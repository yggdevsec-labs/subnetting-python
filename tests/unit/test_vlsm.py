"""Unit tests for VLSM subnet planning."""

import ipaddress

import pytest

from yggdevsec_subnetting.vlsm import plan


def test_plan_allocates_subnets_correctly():
    base = ipaddress.IPv4Network("172.16.0.0/22")
    requests = [400, 180, 40, 18, 2, 2, 2]

    allocations = plan(base, requests)

    expected = [
        "172.16.0.0/23",
        "172.16.2.0/24",
        "172.16.3.0/26",
        "172.16.3.64/27",
        "172.16.3.96/30",
        "172.16.3.100/30",
        "172.16.3.104/30",
    ]

    assert [str(a.network) for a in allocations] == expected


def test_plan_sorts_largest_subnets_first():
    base = ipaddress.IPv4Network("172.16.0.0/22")
    requests = [2, 400, 18]

    allocations = plan(base, requests)

    assert [a.requested_hosts for a in allocations] == [400, 18, 2]
    assert [a.number for a in allocations] == [2, 3, 1]


def test_plan_does_not_overlap_subnets():
    base = ipaddress.IPv4Network("172.16.0.0/22")
    allocations = plan(base, [400, 180, 40, 18, 2, 2, 2])

    for index, allocation in enumerate(allocations):
        for other in allocations[index + 1 :]:
            assert not allocation.network.overlaps(other.network)


def test_plan_rejects_empty_requests():
    base = ipaddress.IPv4Network("172.16.0.0/22")

    with pytest.raises(ValueError, match="Supply at least one host count"):
        plan(base, [])


@pytest.mark.parametrize("hosts", [0, -1, 2**32])
def test_plan_rejects_invalid_host_counts(hosts):
    base = ipaddress.IPv4Network("172.16.0.0/22")

    with pytest.raises(ValueError):
        plan(base, [hosts])


def test_plan_rejects_insufficient_space():
    base = ipaddress.IPv4Network("192.168.1.0/24")

    with pytest.raises(ValueError, match="Not enough space"):
        plan(base, [200, 100])
