"""Command-line interface for the IPv4 subnet calculator."""

import argparse
import sys

from yggdevsec_subnetting.ipv4 import parse_ipv4, parse_network
from yggdevsec_subnetting.output import print_info, print_plan
from yggdevsec_subnetting.vlsm import plan


def main(argv: list[str] | None = None) -> int:
    """Parse CLI arguments and execute the requested command."""
    parser = argparse.ArgumentParser(description="IPv4 subnet information and VLSM planning")

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # Subnet information
    info_parser = subparsers.add_parser(
        "info",
        help="Show details for an IPv4 CIDR",
    )
    info_parser.add_argument(
        "network",
        help="For example 172.16.0.0/22",
    )

    # VLSM planning
    plan_parser = subparsers.add_parser(
        "plan",
        help="Allocate VLSM subnets for host counts",
    )
    plan_parser.add_argument(
        "network",
        help="Parent CIDR, for example 172.16.0.0/22",
    )
    plan_parser.add_argument(
        "hosts",
        type=int,
        nargs="+",
        help="Required hosts per network",
    )

    # IP address membership
    contains_parser = subparsers.add_parser(
        "contains",
        help="Check if an IP belongs to a network",
    )
    contains_parser.add_argument(
        "network",
        help="Network CIDR",
    )
    contains_parser.add_argument(
        "address",
        help="IPv4 address",
    )

    args = parser.parse_args(argv)

    try:
        base = parse_network(args.network)

        if args.command == "info":
            print_info(base)

        elif args.command == "plan":
            allocations = plan(base, args.hosts)
            print_plan(base, allocations)

        elif args.command == "contains":
            address = parse_ipv4(args.address)
            result = "is" if address in base else "is NOT"
            print(f"{address} {result} in {base}")

    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
