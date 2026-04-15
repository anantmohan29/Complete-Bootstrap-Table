"""CLI entry point for secure theHarvester execution."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

from config import OUTPUT_DIR, SOURCE_ALIASES, SUPPORTED_SOURCES
from installer import InstallationError, ensure_harvester_installed, validate_write_permissions

DOMAIN_PATTERN = re.compile(
    r"^(?=.{1,253}$)(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}$"
)
OUTPUT_NAME_PATTERN = re.compile(r"^[A-Za-z0-9_.-]{1,100}$")


def valid_domain(value: str) -> str:
    domain = value.strip().lower()
    if not DOMAIN_PATTERN.fullmatch(domain):
        raise argparse.ArgumentTypeError(
            "Invalid domain format. Example of valid domain: example.com"
        )
    return domain


def valid_source(value: str) -> str:
    source = value.strip().lower()
    if source not in SUPPORTED_SOURCES:
        raise argparse.ArgumentTypeError(
            f"Invalid source '{source}'. Choose one of: {', '.join(sorted(SUPPORTED_SOURCES))}"
        )
    return SOURCE_ALIASES.get(source, source)


def valid_output_name(value: str) -> str:
    output = value.strip()
    if "/" in output or "\\" in output or not OUTPUT_NAME_PATTERN.fullmatch(output):
        raise argparse.ArgumentTypeError(
            "Output filename must be 1-100 chars and contain only letters, numbers, underscore, dash, or dot."
        )
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run theHarvester safely and store structured output files."
    )
    parser.add_argument("--domain", type=valid_domain, help="Target domain, e.g., example.com")
    parser.add_argument("--source", type=valid_source, help="Data source, e.g., google, bing, all")
    parser.add_argument("--output", type=valid_output_name, help="Output base filename")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help=f"Output directory path (default: {OUTPUT_DIR})",
    )
    parser.add_argument(
        "--no-install",
        action="store_true",
        help="Do not auto-install theHarvester if missing.",
    )
    return parser.parse_args()


def prompt_if_missing(namespace: argparse.Namespace) -> argparse.Namespace:
    if not namespace.domain:
        namespace.domain = valid_domain(input("Enter target domain (e.g., example.com): "))
    if not namespace.source:
        namespace.source = valid_source(input("Enter data source (e.g., all, google, bing): "))
    if not namespace.output:
        namespace.output = valid_output_name(input("Enter output filename (without path): "))
    return namespace


def run_harvester(binary_path: str, domain: str, source: str, output_base: Path) -> str:
    command = [
        binary_path,
        "-d",
        domain,
        "-b",
        source,
        "-f",
        str(output_base),
    ]

    print("[+] Executing theHarvester...")
    process = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )

    txt_file = output_base.with_suffix(".txt")
    report_parts = ["=== STDOUT ===", process.stdout.strip()]
    if process.stderr.strip():
        report_parts.extend(["", "=== STDERR ===", process.stderr.strip()])
    txt_file.write_text("\n".join(report_parts) + "\n", encoding="utf-8")

    if process.returncode != 0:
        raise RuntimeError(
            "theHarvester execution failed. See TXT output for details: "
            f"{txt_file}"
        )

    return process.stdout


def main() -> int:
    try:
        args = prompt_if_missing(parse_args())
        output_dir = args.output_dir.resolve()
        validate_write_permissions(output_dir)

        print("[+] Checking theHarvester installation...")
        binary = ensure_harvester_installed(auto_install=not args.no_install)
        print(f"[+] Using theHarvester binary: {binary}")

        output_base = output_dir / args.output
        run_harvester(binary, args.domain, args.source, output_base)

        print("✔ Scan completed")
        html_file = output_base.with_suffix(".html")
        xml_file = output_base.with_suffix(".xml")
        txt_file = output_base.with_suffix(".txt")

        if html_file.exists():
            print(f"✔ Results saved to: {html_file}")
        else:
            print(f"⚠ Expected HTML output not found: {html_file}")

        if xml_file.exists():
            print(f"✔ Results saved to: {xml_file}")
        else:
            print(f"⚠ Expected XML output not found: {xml_file}")

        print(f"✔ Results saved to: {txt_file}")
        return 0
    except KeyboardInterrupt:
        print("Interrupted by user.", file=sys.stderr)
    except (InstallationError, PermissionError, argparse.ArgumentTypeError, RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
    except Exception as exc:  # pragma: no cover
        print(f"Unexpected error: {exc}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
