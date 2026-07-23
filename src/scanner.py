import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from tqdm import tqdm

from src.filters import (
    passes_age_filter,
    passes_size_filter,
    should_exclude_extension,
    should_exclude_path,
)
from src.utils import format_timestamp


def process_file(
    file_path: Path,
    config: dict,
) -> dict | None:
    """Check a file against size/age filters and return its metadata dict, or None if filtered."""
    try:
        stat = file_path.stat()

        if should_exclude_extension(
            file_path,
            config.get("excluded_extensions", []),
        ):
            return None

        if not passes_size_filter(
            stat.st_size,
            config.get("min_file_size_mb", 0),
        ):
            return None

        if not passes_age_filter(
            stat.st_mtime,
            config.get("min_age_days", 0),
        ):
            return None

        return {
            "path": str(file_path),
            "type": "File",
            "size_bytes": stat.st_size,
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "file_created": format_timestamp(stat.st_ctime),
            "last_modified": format_timestamp(stat.st_mtime),
        }

    except (PermissionError, FileNotFoundError, OSError):
        return None


def collect_files(
    root_path: str | Path,
    excluded_paths: list[str],
) -> list[Path]:
    """Recursively collect all files under root_path that are not excluded."""
    files = []
    root = Path(root_path)

    for item in root.rglob("*"):
        try:
            if should_exclude_path(item, excluded_paths):
                continue

            if item.is_file():
                files.append(item)

        except (PermissionError, OSError):
            continue

    return files


def scan_files(
    config: dict,
    logger: logging.Logger,
) -> list[dict]:
    """Scan and process files in parallel using the provided configuration."""
    logger.info("Collecting files...")

    files = collect_files(
        config["scan_root"],
        config.get("excluded_paths", []),
    )

    logger.info(f"Found {len(files)} files")

    with ThreadPoolExecutor(
        max_workers=config.get("max_workers", 8)
    ) as executor:
        results = list(
            tqdm(
                executor.map(
                    lambda f: process_file(f, config),
                    files,
                ),
                total=len(files),
                desc="Scanning",
            )
        )

    records = [r for r in results if r]
    logger.info(f"Valid records: {len(records)}")

    return records
