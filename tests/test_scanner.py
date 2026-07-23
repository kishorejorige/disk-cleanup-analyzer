import logging

from src.scanner import collect_files, process_file, scan_files


def test_process_file(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_bytes(b"\0" * 1024 * 1024 * 10)  # 10 MB

    config = {
        "excluded_extensions": [".dll"],
        "min_file_size_mb": 5,
        "min_age_days": 0,
    }

    res = process_file(file_path, config)
    assert res is not None
    assert res["path"] == str(file_path)
    assert res["size_mb"] == 10.0
    assert res["size_bytes"] == 1024 * 1024 * 10
    assert "file_created" in res
    assert "last_modified" in res


def test_process_file_filtered_by_size(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_bytes(b"\0" * 1024 * 1024 * 2)  # 2 MB

    config = {
        "excluded_extensions": [".dll"],
        "min_file_size_mb": 5,
        "min_age_days": 0,
    }

    res = process_file(file_path, config)
    assert res is None


def test_collect_files(tmp_path):
    # Setup files:
    # tmp_path
    #  ├── doc.txt
    #  ├── windows_backup (should exclude)
    #  │    └── note.txt
    #  └── sub
    #       └── file.log

    doc = tmp_path / "doc.txt"
    doc.touch()

    win_backup = tmp_path / "windows_backup"
    win_backup.mkdir()
    note = win_backup / "note.txt"
    note.touch()

    sub = tmp_path / "sub"
    sub.mkdir()
    log = sub / "file.log"
    log.touch()

    files = collect_files(tmp_path, excluded_paths=["windows_backup"])

    file_paths = [str(f) for f in files]
    assert str(doc) in file_paths
    assert str(log) in file_paths
    assert str(note) not in file_paths


def test_scan_files(tmp_path):
    logger = logging.getLogger("test_scanner")
    logger.setLevel(logging.WARNING)

    file1 = tmp_path / "large.zip"
    file2 = tmp_path / "small.txt"
    file3 = tmp_path / "excluded.dll"

    file1.write_bytes(b"\0" * 1024 * 1024 * 15)  # 15 MB
    file2.write_bytes(b"\0" * 100)               # 100 Bytes
    file3.write_bytes(b"\0" * 1024 * 1024 * 20)  # 20 MB

    config = {
        "scan_root": str(tmp_path),
        "excluded_paths": [],
        "excluded_extensions": [".dll"],
        "min_file_size_mb": 10,
        "min_age_days": 0,
        "max_workers": 2,
    }

    records = scan_files(config, logger)

    assert len(records) == 1
    assert records[0]["path"] == str(file1)
    assert records[0]["size_mb"] == 15.0
    assert records[0]["size_bytes"] == 15 * 1024 * 1024
