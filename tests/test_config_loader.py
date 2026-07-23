import json

import pytest

from src.config_loader import (
    ConfigError,
    create_default_config,
    load_config,
    validate_config,
)


def test_create_default_config(tmp_path):
    config_file = tmp_path / "config.json"
    create_default_config(config_file)

    assert config_file.exists()
    with open(config_file, encoding="utf-8") as f:
        data = json.load(f)

    assert data["scan_root"] == "."
    assert "output_csv" in data


def test_load_valid_config(tmp_path):
    config_file = tmp_path / "config.json"
    config_data = {
        "scan_root": str(tmp_path),
        "output_csv": str(tmp_path / "report.csv"),
        "min_file_size_mb": 5,
        "min_age_days": 10,
    }

    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config_data, f)

    config = load_config(config_file)
    assert config["scan_root"] == str(tmp_path)
    assert config["min_file_size_mb"] == 5


def test_load_config_missing_file():
    with pytest.raises(ConfigError, match="Configuration file not found"):
        load_config("non_existent_config_file_xyz.json")


def test_load_config_invalid_json(tmp_path):
    config_file = tmp_path / "bad.json"
    config_file.write_text("{invalid_json:")

    with pytest.raises(ConfigError, match="Invalid JSON configuration"):
        load_config(config_file)


def test_validate_config_missing_fields():
    with pytest.raises(ConfigError, match="Missing required config field"):
        validate_config({})


def test_validate_config_invalid_scan_root(tmp_path):
    config = {
        "scan_root": "invalid_directory_path_12345",
        "output_csv": "report.csv",
        "min_file_size_mb": 10,
        "min_age_days": 5,
    }
    with pytest.raises(ConfigError, match="Config scan_root does not exist"):
        validate_config(config)

    # Exists but is not a directory
    test_file = tmp_path / "file.txt"
    test_file.touch()
    config["scan_root"] = str(test_file)
    with pytest.raises(ConfigError, match="Config scan_root is not a directory"):
        validate_config(config)


def test_validate_config_negative_values(tmp_path):
    config = {
        "scan_root": str(tmp_path),
        "output_csv": "report.csv",
        "min_file_size_mb": -1,
        "min_age_days": 5,
    }
    with pytest.raises(ConfigError, match="min_file_size_mb cannot be negative"):
        validate_config(config)

    config["min_file_size_mb"] = 10
    config["min_age_days"] = -5
    with pytest.raises(ConfigError, match="min_age_days cannot be negative"):
        validate_config(config)


def test_validate_config_type_validations(tmp_path):
    config = {
        "scan_root": str(tmp_path),
        "output_csv": "report.csv",
        "min_file_size_mb": "not_a_number",
        "min_age_days": 5,
    }
    with pytest.raises(ConfigError, match="min_file_size_mb must be a number"):
        validate_config(config)

    config["min_file_size_mb"] = 10
    config["max_workers"] = "eight"
    with pytest.raises(ConfigError, match="max_workers must be an integer"):
        validate_config(config)

    config["max_workers"] = 0
    with pytest.raises(ConfigError, match="max_workers must be greater than zero"):
        validate_config(config)


def test_load_config_with_override(tmp_path):
    config_file = tmp_path / "config.json"
    config_data = {
        "scan_root": "invalid_path_but_ignored_due_to_override",
        "output_csv": str(tmp_path / "report.csv"),
        "min_file_size_mb": 5,
        "min_age_days": 10,
    }

    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config_data, f)

    # Passing valid override should load successfully and validate
    config = load_config(config_file, scan_root_override=str(tmp_path))
    assert config["scan_root"] == str(tmp_path)
