#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "[!] python3 is required but not installed."
  exit 1
fi

if command -v apt-get >/dev/null 2>&1; then
  echo "[+] Installing theHarvester package (if missing)..."
  if [ "$(id -u)" -ne 0 ]; then
    sudo apt-get update
    sudo apt-get install -y theharvester
  else
    apt-get update
    apt-get install -y theharvester
  fi
else
  echo "[!] apt-get not found. Install theHarvester manually for your distro."
fi

mkdir -p outputs
chmod +x main.py

echo "[+] Setup complete."
echo "[+] Run: python3 main.py --domain example.com --source all --output result"
