# theHarvester CLI App

A production-ready Python CLI wrapper for running [theHarvester](https://github.com/laramies/theHarvester) on Linux (Ubuntu/Kali) with secure argument handling, auto-install support, and structured output files.

## 1) Project Overview

This app:
- Checks whether `theHarvester` is installed.
- Installs it automatically with `apt` if missing.
- Accepts user input for domain, source, and output filename.
- Runs the tool with `subprocess` safely (no shell injection).
- Saves output to HTML, XML, and TXT references.
- Provides clear status messages and error handling.

## 2) Folder Structure

```text
harvester_app/
│── main.py
│── installer.py
│── config.py
│── requirements.txt
│── install.sh
│── README.md
│── outputs/
```

## 3) Source Code

### `config.py`
- Shared constants (`OUTPUT_DIR`, `SUPPORTED_SOURCES`).

### `installer.py`
- Detects `theHarvester` binary.
- Installs using `apt-get` + optional `sudo`.
- Validates output directory write permission.

### `main.py`
- Parses CLI arguments (`--domain`, `--source`, `--output`, `--output-dir`).
- Prompts interactively if required values are missing.
- Validates/sanitizes input:
  - strict domain regex
  - allowlisted source values
  - safe output filename pattern
- Executes `theHarvester` securely with argument list.
- Writes TXT execution output (`stdout` + `stderr`) and prints expected HTML/XML/TXT paths.

## 4) Installation Instructions

From the repository root:

```bash
cd harvester_app
chmod +x install.sh
./install.sh
```

Manual alternative:

```bash
sudo apt-get update
sudo apt-get install -y theharvester
```

## 5) Usage Guide

### Basic CLI use

```bash
python3 main.py --domain example.com --source all --output result
```

### Interactive prompts (if args omitted)

```bash
python3 main.py
```

### Optional output directory

```bash
python3 main.py --domain example.com --source bing --output scan1 --output-dir ./outputs
```

### Disable auto-install

```bash
python3 main.py --domain example.com --source all --output result --no-install
```

## 6) Sample Output

```text
[+] Checking theHarvester installation...
[+] Using theHarvester binary: /usr/bin/theHarvester
[+] Executing theHarvester...
✔ Scan completed
✔ Results saved to: /.../outputs/result.html
✔ Results saved to: /.../outputs/result.xml
✔ Results saved to: /.../outputs/result.txt
```

## 7) Run in VS Code

1. Open folder: `harvester_app` in VS Code.
2. Open terminal in VS Code.
3. Run setup:
   ```bash
   chmod +x install.sh && ./install.sh
   ```
4. Execute app:
   ```bash
   python3 main.py --domain example.com --source all --output result
   ```

## 8) Future Enhancements

- Add JSON output export.
- Add optional FastAPI web interface.
- Add Dockerfile and containerized execution profile.
