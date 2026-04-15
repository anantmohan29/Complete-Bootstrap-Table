"""Install and discovery helpers for theHarvester."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional


HARVESTER_CANDIDATES = ("theHarvester", "theharvester")


class InstallationError(RuntimeError):
    """Raised when installation cannot be completed."""


def detect_harvester_binary() -> Optional[str]:
    """Return absolute executable path if theHarvester is installed."""
    for candidate in HARVESTER_CANDIDATES:
        path = shutil.which(candidate)
        if path:
            return path
    return None


def _run_install_command(command: list[str]) -> None:
    process = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        env=os.environ.copy(),
    )
    if process.returncode != 0:
        detail = process.stderr.strip() or process.stdout.strip() or "unknown installation error"
        raise InstallationError(detail)


def ensure_harvester_installed(auto_install: bool = True) -> str:
    """Ensure theHarvester is available and optionally install with apt."""
    existing = detect_harvester_binary()
    if existing:
        return existing

    if not auto_install:
        raise InstallationError("theHarvester is not installed.")

    apt_get = shutil.which("apt-get")
    if not apt_get:
        raise InstallationError("apt-get not found. Install theHarvester manually.")

    if not hasattr(os, "geteuid"):
        raise InstallationError(
            "Automatic installation is supported only on Linux systems. "
            "Please install theHarvester manually for your operating system."
        )

    install_commands = []
    if os.geteuid() != 0:
        sudo = shutil.which("sudo")
        if not sudo:
            raise InstallationError("Root privileges required for installation (sudo not found).")
        install_commands.extend(
            [
                [sudo, apt_get, "update"],
                [sudo, apt_get, "install", "-y", "theharvester"],
            ]
        )
    else:
        install_commands.extend(
            [
                [apt_get, "update"],
                [apt_get, "install", "-y", "theharvester"],
            ]
        )

    for command in install_commands:
        _run_install_command(command)

    installed = detect_harvester_binary()
    if not installed:
        raise InstallationError(
            "Installation command completed but theHarvester binary was not found in PATH."
        )

    return installed


def validate_write_permissions(path: Path) -> None:
    """Raise if directory cannot be written."""
    path.mkdir(parents=True, exist_ok=True)
    if not os.access(path, os.W_OK):
        raise PermissionError(f"Write permission denied for directory: {path}")


if __name__ == "__main__":
    try:
        binary = ensure_harvester_installed(auto_install=True)
        print(f"theHarvester available at: {binary}")
    except Exception as exc:  # pragma: no cover
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
