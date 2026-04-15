"""Configuration constants for theHarvester CLI wrapper."""

from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = APP_DIR / "outputs"

SUPPORTED_SOURCES = {
    "all",
    "anubis",
    "baidu",
    "bevigil",
    "bing",
    "bingapi",
    "binaryedge",
    "brave",
    "bufferoverun",
    "censys",
    "certspotter",
    "criminalip",
    "crtsh",
    "dnsdumpster",
    "duckduckgo",
    "github-code",
    "google",
    "hackertarget",
    "hunter",
    "intelx",
    "netlas",
    "otx",
    "rapiddns",
    "securityTrails",
    "sitedossier",
    "subdomaincenter",
    "subdomainfinderc99",
    "threatminer",
    "urlscan",
    "virustotal",
    "yahoo",
    "zoomeye",
}
