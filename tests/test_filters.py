from pathlib import Path

from src.filters import (
    passes_age_filter,
    passes_size_filter,
    should_exclude_extension,
    should_exclude_path,
)


def test_should_exclude_path():
    excluded = ["Windows", "System Volume Information", "cache"]

    # Matching cases
    assert should_exclude_path(Path("/Users/test/Windows/System32"), excluded) is True
    assert should_exclude_path(Path("/var/log/my-cache-dir/file.txt"), excluded) is True
    assert should_exclude_path(Path("C:\\System Volume Information"), excluded) is True

    # Case insensitivity
    assert should_exclude_path(Path("/users/test/windows"), excluded) is True

    # Non-matching cases
    assert should_exclude_path(Path("/users/test/documents/notes.txt"), excluded) is False
    assert should_exclude_path(Path("/mnt/d/projects/disk_cleanup_analyzer"), excluded) is False


def test_should_exclude_extension():
    excluded = [".dll", ".sys", ".tmp"]

    assert should_exclude_extension(Path("test.dll"), excluded) is True
    assert should_exclude_extension(Path("system.SYS"), excluded) is True  # case insensitive
    assert should_exclude_extension(Path("temp.tmp"), excluded) is True

    assert should_exclude_extension(Path("main.py"), excluded) is False
    assert should_exclude_extension(Path("no_extension"), excluded) is False


def test_passes_size_filter():
    # min_size_mb = 10 (10 MB = 10,485,760 Bytes)
    min_size = 10

    assert passes_size_filter(10 * 1024 * 1024, min_size) is True
    assert passes_size_filter(20 * 1024 * 1024, min_size) is True
    assert passes_size_filter(5 * 1024 * 1024, min_size) is False
    assert passes_size_filter(0, min_size) is False


def test_passes_age_filter():
    import time

    now = time.time()
    one_day_sec = 86400

    # File modified 10 days ago. Filter demands at least 5 days age. Should pass.
    assert passes_age_filter(now - (10 * one_day_sec), 5) is True

    # File modified 2 days ago. Filter demands at least 5 days age. Should fail.
    assert passes_age_filter(now - (2 * one_day_sec), 5) is False

    # Edge case: min_age_days = 0 should pass everything in the past/present
    assert passes_age_filter(now, 0) is True
