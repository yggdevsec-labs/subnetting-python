# YggDevSec Subnetting

A command-line tool for IPv4 subnet calculations and Variable Length Subnet Masking (VLSM) planning, written in Python.

The tool provides subnet details, allocates subnets based on host requirements, and checks whether an IPv4 address belongs to a network.

## Features

- Display network address, CIDR prefix, subnet mask, address range, and broadcast address.
- Show the historical IPv4 address class (A–E), including special handling for `0/8` and `127/8`.
- Plan multiple VLSM subnets, allocating the largest host requirements first.
- Preserve each host request's original number in the VLSM output.
- Detect insufficient address space and reject invalid IPv4 inputs.
- Check whether an IPv4 address belongs to a specified network.
- Handle `/31` and `/32` usable addresses in the `info` command.

**Note:** IPv4 address classes are legacy terminology. CIDR prefixes determine subnet sizes in modern networks. The VLSM planner uses traditional subnetting with reserved network and broadcast addresses and a minimum subnet size of `/30`.

## Requirements

- Python 3.11 or newer
- pip

Runtime functionality uses Python's standard library. Development tools are installed separately through the `dev` extra.

## Installation

Clone the repository after it has been published, or open the project directory locally. From the repository root, create and activate a virtual environment.

**Windows (Command Prompt):**

```cmd
py -m venv .venv
.venv\Scripts\activate
python -m pip install -e ".[dev]"
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

If you only need to run the application and do not need the test or lint tools, install it with `python -m pip install -e .` instead.

## Usage

Run the application as a Python module:

```console
python -m yggdevsec_subnetting --help
```

### Subnet information

```console
python -m yggdevsec_subnetting info 172.16.0.0/22
```

Example information:

```text
Network           172.16.0.0
IP Class (legacy) B
CIDR              /22
Subnet mask       255.255.252.0
Total addresses   1024
Usable hosts      1022
First usable IP   172.16.0.1
Last usable IP    172.16.3.254
Broadcast         172.16.3.255
```

### VLSM planning

Provide the parent network followed by the required host counts:

```console
python -m yggdevsec_subnetting plan 172.16.0.0/22 400 180 40 18 2 2 2
```

Example allocations:

| # | Hosts | Network (CIDR) | Subnet mask | First usable | Last usable | Broadcast |
|---|------:|----------------|-------------|--------------|-------------|-----------|
| 1 | 400 | 172.16.0.0/23 | 255.255.254.0 | 172.16.0.1 | 172.16.1.254 | 172.16.1.255 |
| 2 | 180 | 172.16.2.0/24 | 255.255.255.0 | 172.16.2.1 | 172.16.2.254 | 172.16.2.255 |
| 3 | 40 | 172.16.3.0/26 | 255.255.255.192 | 172.16.3.1 | 172.16.3.62 | 172.16.3.63 |
| 4 | 18 | 172.16.3.64/27 | 255.255.255.224 | 172.16.3.65 | 172.16.3.94 | 172.16.3.95 |
| 5 | 2 | 172.16.3.96/30 | 255.255.255.252 | 172.16.3.97 | 172.16.3.98 | 172.16.3.99 |
| 6 | 2 | 172.16.3.100/30 | 255.255.255.252 | 172.16.3.101 | 172.16.3.102 | 172.16.3.103 |
| 7 | 2 | 172.16.3.104/30 | 255.255.255.252 | 172.16.3.105 | 172.16.3.106 | 172.16.3.107 |

Requests are allocated from largest to smallest to make efficient use of the available address space. The `#` column identifies the position of each request in the original input.

### Check whether an IP address is in a subnet

```console
python -m yggdevsec_subnetting contains 192.168.1.0/24 192.168.1.10
```

Expected output:

```text
192.168.1.10 is in 192.168.1.0/24
```

## Project structure

```text
subnetting-python/
├── src/
│   └── yggdevsec_subnetting/
│       ├── __init__.py
│       ├── __main__.py    # Module entry point
│       ├── cli.py         # Argument parsing and commands
│       ├── ipv4.py        # IPv4 parsing and subnet calculations
│       ├── output.py      # Terminal output formatting
│       └── vlsm.py        # VLSM allocation
├── tests/
│   ├── test_cli.py
│   ├── test_ipv4.py
│   └── test_vlsm.py
├── .gitignore
├── pyproject.toml
└── README.md
```

## Development and testing

Install the optional development dependencies (`pytest`, `pytest-cov`, and `ruff`):

```console
python -m pip install -e ".[dev]"
```

Run the automated tests:

```console
python -m pytest -v
```

Check lint rules and formatting:

```console
python -m ruff check .
python -m ruff format --check .
```

Measure test coverage:

```console
python -m pytest --cov=yggdevsec_subnetting --cov-report=term-missing
```

Enforce a minimum total coverage of 90%:

```console
python -m pytest --cov=yggdevsec_subnetting --cov-report=term-missing --cov-fail-under=90
```

At the time of development, the test suite reported **97% total statement coverage**. Coverage measures executed code, not the absence of bugs.

## Troubleshooting

If an editable installation fails while installing build dependencies, first check that pip and the build backend are available and up to date. As a local workaround, you can install `setuptools` and use the already-installed build backend:

```console
python -m pip install "setuptools>=68"
python -m pip install -e ".[dev]" --no-build-isolation
```

This workaround bypasses build isolation and is not required for environments where the normal installation succeeds.

## Project status

This project is under active development as part of **YggDevSec Labs**. The repository is intended to remain private until it is ready for publication.

