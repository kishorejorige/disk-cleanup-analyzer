from datetime import datetime


def readable_size(size_bytes: int | float) -> str:
    """Format size in bytes to a human-readable string representation."""
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)

    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

    return f"{size:.2f} PB"


def format_timestamp(ts: float) -> str:
    """Format a unix timestamp into a standard date-time string."""
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
