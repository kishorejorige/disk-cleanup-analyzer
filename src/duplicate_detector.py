import hashlib
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from tqdm import tqdm


def calculate_hash(
    file_path: Path,
    chunk_size: int = 1024 * 1024,
) -> tuple[str, str] | None:
    """Calculate the SHA256 hash of a file. Returns (file_path_str, sha256_hex) or None on failure."""
    sha = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                sha.update(chunk)

        return (
            str(file_path),
            sha.hexdigest(),
        )

    except Exception:
        return None


def find_duplicates(
    file_paths: list[Path],
    workers: int = 8,
) -> dict[str, list[str]]:
    """Find duplicate files in parallel using SHA256 hashes.

    Returns a dict mapping hash values to lists of matching file paths,
    sorted deterministically.
    """
    hash_map: dict[str, list[str]] = defaultdict(list)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(
            tqdm(
                executor.map(calculate_hash, file_paths),
                total=len(file_paths),
                desc="Hashing",
            )
        )

    for result in results:
        if result is None:
            continue

        file_path, hash_value = result
        hash_map[hash_value].append(file_path)

    # Sort file paths within each duplicate group and sort groups by hash for absolute determinism
    return {
        h: sorted(files)
        for h, files in sorted(hash_map.items())
        if len(files) > 1
    }

