"""VLSM subnet planning and allocation."""

import ipaddress
from dataclasses import dataclass

from yggdevsec_subnetting.ipv4 import prefix_for_hosts


@dataclass(frozen=True)
class Allocation:
    number: int
    requested_hosts: int
    network: ipaddress.IPv4Network


def plan(
    base: ipaddress.IPv4Network,
    requests: list[int],
) -> list[Allocation]:
    """Allocate the largest subnets first within the parent network."""
    if not requests:
        raise ValueError("Supply at least one host count.")

    ordered = sorted(
        enumerate(requests, start=1),
        key=lambda item: (-item[1], item[0]),
    )

    cursor = int(base.network_address)
    limit = int(base.broadcast_address) + 1
    result: list[Allocation] = []

    for number, hosts in ordered:
        prefix = prefix_for_hosts(hosts)
        block_size = 1 << (32 - prefix)

        # Align the subnet to its required block boundary.
        start = ((cursor + block_size - 1) // block_size) * block_size

        if start + block_size > limit:
            raise ValueError(
                f"Not enough space in {base}: request #{number} "
                f"({hosts} hosts) needs a /{prefix} subnet."
            )

        subnet = ipaddress.IPv4Network((start, prefix))

        result.append(Allocation(number, hosts, subnet))
        cursor = start + block_size

    return result
