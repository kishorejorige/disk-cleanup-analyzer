from pathlib import Path

from src.utils import format_timestamp


def calculate_folder_sizes(root_path: str | Path) -> list[dict]:
    """Calculate size and metadata for all folders under the root path.

    This uses an optimized bottom-up traversal to calculate sizes in O(N * D) time,
    avoiding the O(N^2) overhead of redundant scanning.
    """
    root = Path(root_path).resolve()
    dir_sizes: dict[Path, int] = {}
    dir_stats: dict[Path, OSError | None] = {}
    folder_records = []

    # Step 1: Discover all directories and store stats
    for folder in root.rglob("*"):
        try:
            if folder.is_dir():
                dir_sizes[folder] = 0
                dir_stats[folder] = folder.stat()
        except (PermissionError, FileNotFoundError, OSError):
            continue

    # Step 2: Accumulate file sizes bottom-up
    for item in root.rglob("*"):
        try:
            if item.is_file():
                size = item.stat().st_size
                for parent in item.parents:
                    if parent in dir_sizes:
                        dir_sizes[parent] += size
                    if parent == root:
                        break
        except (PermissionError, FileNotFoundError, OSError):
            continue

    # Step 3: Format records
    for folder, size_bytes in dir_sizes.items():
        stat = dir_stats.get(folder)
        if not stat:
            continue

        try:
            folder_records.append(
                {
                    "path": str(folder),
                    "type": "Folder",
                    "size_mb": round(size_bytes / (1024 * 1024), 2),
                    "file_created": format_timestamp(stat.st_ctime),
                    "last_modified": format_timestamp(stat.st_mtime),
                }
            )
        except (PermissionError, FileNotFoundError, OSError):
            continue

    folder_records.sort(
        key=lambda x: x["size_mb"],
        reverse=True,
    )

    return folder_records
