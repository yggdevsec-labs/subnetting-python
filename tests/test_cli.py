"""Unit tests for the subnetting CLI."""

import pytest

from yggdevsec_subnetting.cli import main


def test_info_command(capsys):
    result = main(["info", "172.16.0.0/22"])
    output = capsys.readouterr()

    assert result == 0
    assert "172.16.0.0" in output.out
    assert "255.255.252.0" in output.out
    assert "1024" in output.out
    assert "IP Class (legacy)" in output.out


def test_plan_command(capsys):
    result = main(["plan", "172.16.0.0/22", "400", "180", "40", "18", "2", "2", "2"])
    output = capsys.readouterr()

    assert result == 0
    assert "172.16.0.0/23" in output.out
    assert "172.16.2.0/24" in output.out
    assert "172.16.3.104/30" in output.out


@pytest.mark.parametrize(
    ("address", "expected"),
    [
        ("192.168.1.10", "is in"),
        ("192.168.2.10", "is NOT in"),
    ],
)
def test_contains_command(capsys, address, expected):
    result = main(["contains", "192.168.1.0/24", address])
    output = capsys.readouterr()

    assert result == 0
    assert expected in output.out


def test_invalid_network(capsys):
    result = main(["info", "invalid"])
    output = capsys.readouterr()

    assert result == 1
    assert "Error:" in output.err


def test_invalid_ipv4_address(capsys):
    result = main(["contains", "192.168.1.0/24", "invalid"])
    output = capsys.readouterr()

    assert result == 1
    assert "Error:" in output.err


def test_plan_insufficient_space(capsys):
    result = main(["plan", "192.168.1.0/24", "200", "100"])
    output = capsys.readouterr()

    assert result == 1
    assert "Not enough space" in output.err
