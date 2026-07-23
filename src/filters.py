from datetime import datetime
from pathlib import Path


def should_exclude_path(
    path: Path,
    excluded_paths: list[str],
) -> bool:
    """Check if the path string contains any of the excluded path substrings (case-insensitive)."""
    path_str = str(path).lower()
    return any(
        excluded.lower() in path_str
        for excluded in excluded_paths
    )


def should_exclude_extension(
    path: Path,
    excluded_extensions: list[str],
) -> bool:
    """Check if the file suffix is in the excluded extensions list (case-insensitive)."""
    return path.suffix.lower() in [ext.lower() for ext in excluded_extensions]


def passes_size_filter(
    size_bytes: int,
    min_size_mb: int | float,
) -> bool:
    """Return True if the file size is greater than or equal to the minimum size in MB."""
    return size_bytes >= min_size_mb * 1024 * 1024


def passes_age_filter(
    modified_time: float,
    min_age_days: int | float,
) -> bool:
    """Return True if the last modification age of the file is greater than or equal to min_age_days."""
    age_days = (datetime.now().timestamp() - modified_time) / 86400
    return age_days >= min_age_days
