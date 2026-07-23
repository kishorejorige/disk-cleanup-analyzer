# Disk Cleanup Analyzer

[![CI](https://github.com/kishorejorige/disk-cleanup-analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/kishorejorige/disk-cleanup-analyzer/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)

A lightweight, read-only command-line utility for local storage analysis, duplicate file identification, and directory size reports. It is built to help developers and power users identify space-hogging files and directory trees without any risk of accidental data deletion.

---

> [!IMPORTANT]
> **Safety Statement: Read-Only Operations**
> This tool is **strictly read-only**. It analyzes your disk space, detects duplicate content (via SHA256 hashes), and outputs structured HTML and CSV reports. It **never** deletes, moves, or alters any of your files or folders under any circumstance.

---

## Features

- 🔍 **Parallel File Scanning:** Fast multi-threaded local disk scanning using python's `concurrent.futures`.
- 📁 **Optimized Folder Size Analysis:** Bottom-up directory traversal to calculate folder sizes in $O(N \cdot D)$ time complexity.
- 👥 **SHA256 Duplicate Detection:** Parallel hashing of files to detect identical files, sorted deterministically.
- ⚙️ **Configurable Filters & Exclusions:** Exclude specific directories, skip file suffixes, and apply age or size thresholds.
- 📊 **Rich HTML & CSV Reports:** Generates clean, responsive HTML reports sorted by file size alongside raw CSV data.
- 💻 **Robust CLI Interface:** Command-line argument overrides for configuration files, root paths, and output targets.

---

## Project Structure

```text
disk_cleanup_analyzer/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions continuous integration workflow
├── config/
│   └── config.json            # JSON application configuration parameters
├── logs/
│   └── scanner.log            # Scanner run log outputs
├── reports/
│   ├── disk_report.csv        # Detailed tabular file report
│   ├── disk_report.html       # Clean browser-viewable file report
│   ├── duplicates.csv         # List of duplicate files grouped by SHA256
│   └── folders.csv            # Summary list of folders sorted by size
├── src/
│   ├── __init__.py
│   ├── config_loader.py       # JSON configuration parser and type validator
│   ├── duplicate_detector.py  # Threaded duplicate locator (SHA256)
│   ├── exporter.py            # CSV report generation utilities
│   ├── filters.py             # Size, age, extension, and path exclusion filters
│   ├── folder_analyzer.py     # Directory size bottom-up accumulator
│   ├── html_report.py         # Static HTML reporter
│   ├── logger.py              # Centralized logging configuration
│   └── utils.py               # Shared utility tools (e.g. timestamp formatting)
├── tests/
│   ├── test_config_loader.py
│   ├── test_duplicate_detector.py
│   ├── test_exporter.py
│   ├── test_filters.py
│   ├── test_folder_analyzer.py
│   ├── test_html_report.py
│   ├── test_logger.py
│   ├── test_scanner.py
│   └── test_utils.py
├── LICENSE                    # MIT License
├── pyproject.toml             # Project metadata, Ruff, and Pytest configuration
├── README.md
└── uv.lock                    # Locked project dependencies
```

---

## Requirements

- **Python:** `>= 3.11`
- **Package Manager:** `uv` (recommended for lighting fast installs and lockfile management)

---

## Installation & Setup

1. **Install `uv`** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone the Repository** and navigate to it:
   ```bash
   git clone https://github.com/kishorejorige/disk-cleanup-analyzer.git
   cd disk-cleanup-analyzer
   ```

3. **Install Dependencies** (automatically sets up a virtual environment):
   ```bash
   uv sync --dev
   ```

---

## Configuration

A configuration file (`config/config.json`) determines filters, limits, and report scopes.

```json
{
  "scan_root": ".",
  "output_csv": "reports/disk_report.csv",
  "output_html": "reports/disk_report.html",
  "excluded_paths": [
    "$Recycle.Bin",
    "System Volume Information",
    ".git",
    ".venv"
  ],
  "excluded_extensions": [
    ".dll",
    ".sys"
  ],
  "min_file_size_mb": 10,
  "min_age_days": 0,
  "max_workers": 8,
  "enable_duplicate_detection": true,
  "enable_folder_analysis": true,
  "top_n_files": 100
}
```

### Config Options Description
- `scan_root`: Directory directory to scan by default.
- `excluded_paths`: Path segments that should exclude files (case-insensitive substring check).
- `excluded_extensions`: File suffixes that will be ignored (e.g. `.sys`).
- `min_file_size_mb`: Ignore files smaller than this size in megabytes.
- `min_age_days`: Only include files older than this (last modified date minus current date).
- `max_workers`: Number of worker threads to use for parallel checks and hashes.
- `enable_duplicate_detection`: Toggle SHA256 duplicate content detection.
- `enable_folder_analysis`: Toggle folder size sorting analysis.

---

## CLI Usage

Run the scanner using `main.py`. The program supports command line overrides:

```bash
uv run python main.py [options]
```

### Options

| Flag | Description | Example |
|------|-------------|---------|
| `--config` | Path to custom config file | `uv run python main.py --config my_config.json` |
| `--scan-root` | Override the scan directory in config | `uv run python main.py --scan-root ./src` |
| `--output-dir` | Target directory for all output reports | `uv run python main.py --output-dir reports/custom` |
| `--version` | Display version information | `uv run python main.py --version` |

---

## Example Run Command

Perform an analysis of the `./src` folder, placing logs under `logs/` and all reports under `reports/src_scan/`:

```bash
uv run python main.py --scan-root ./src --output-dir reports/src_scan
```

### Expected Output
```text
Duplicate Groups: 0
Folders analyzed: 2
Files reported: 9
```

---

## Development & Verification

Verify code style and run tests using standard commands:

### Running Tests
The project features a comprehensive unit test suite written with `pytest`. It scans only temporary test directories and executes in seconds.

```bash
uv run pytest
```

### Linting & Formatting
We use `Ruff` for ultra-fast styling checks and formatting.

```bash
uv run ruff check .
```

---

## Limitations

- **Symbolic Links:** Symbolic links are resolved as normal paths but target files outside of the scan root are skipped depending on how standard library matches them.
- **Permission Limitations:** Files and directories with restricted read permissions are skipped silently and listed in logs.
- **Memory Footprint:** Keeps a file metadata dictionary for reporting in memory, which scales linearly with the number of files scanned.

---

## Privacy & Security

All hash calculations and file metadata extraction are processed entirely **locally**. No information, directory structures, paths, or file contents are sent online or to any external server.

---

## Roadmap

- [ ] Add interactive console dashboards (using `rich` or `curses`).
- [ ] Export reports in JSON and Markdown formats.
- [ ] Support wildcard glob patterns in `excluded_paths`.
- [ ] Implement incremental scan caches for large disk scanning.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

**Kishore**
*Python Developer*
- GitHub: [https://github.com/kishorejorige](https://github.com/kishorejorige)
