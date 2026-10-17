"""Terminal output formatting for IPv4 subnet information and VLSM plans."""

import ipaddress

from yggdevsec_subnetting.ipv4 import get_ip_class, usable_range
from yggdevsec_subnetting.vlsm import Allocation


def print_info(network: ipaddress.IPv4Network) -> None:
    """Print detailed information about an IPv4 subnet."""
    first, last, hosts = usable_range(network)

    broadcast = str(network.broadcast_address) if network.prefixlen <= 30 else "N/A (/31 or /32)"

    fields = (
        ("Network (CIDR)", str(network)),
        ("IP Class (legacy)", get_ip_class(network)),
        ("Subnet mask", str(network.netmask)),
        ("Total addresses", str(network.num_addresses)),
        ("Usable hosts", str(hosts)),
        ("First usable IP", first),
        ("Last usable IP", last),
        ("Broadcast", broadcast),
    )

    for label, value in fields:
        print(f"{label:<17} {value}")


def print_plan(
    base: ipaddress.IPv4Network,
    allocations: list[Allocation],
) -> None:
    """Print a formatted table of VLSM subnet allocations."""
    print(f"Base network: {base}\n")
    print(f"IP Class (legacy): {get_ip_class(base)}\n")

    header = (
        f"{'#':>2} {'Hosts':>6} {'Network (CIDR)':<18} "
        f"{'Mask':<18} {'First usable':<16} "
        f"{'Last usable':<16} Broadcast"
    )

    print(header)
    print("-" * len(header))

    for allocation in allocations:
        network = allocation.network
        first, last, _ = usable_range(network)

        print(
            f"{allocation.number:>2} "
            f"{allocation.requested_hosts:>6} "
            f"{str(network):<18} "
            f"{str(network.netmask):<18} "
            f"{first:<16} "
            f"{last:<16} "
            f"{network.broadcast_address}"
        )
