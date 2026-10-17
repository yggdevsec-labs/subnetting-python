"""Integration tests for the Python module entry point."""

import subprocess
import sys


def test_module_entrypoint_info():
    """Verify that the installed Python module starts correctly."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "yggdevsec_subnetting",
            "info",
            "172.16.0.0/22",
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=15,
    )

    assert result.returncode == 0, result.stderr
    assert "172.16.0.0" in result.stdout
    assert "255.255.252.0" in result.stdout
    assert "1024" in result.stdout
