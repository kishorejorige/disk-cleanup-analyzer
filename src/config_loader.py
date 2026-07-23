import json
from pathlib import Path

DEFAULT_CONFIG = {
    "scan_root": ".",
    "output_csv": "reports/disk_report.csv",
    "output_html": "reports/disk_report.html",
    "excluded_paths": [
        "Windows",
        "Program Files",
        "Program Files (x86)",
        "ProgramData",
        "$Recycle.Bin",
        "System Volume Information",
    ],
    "excluded_extensions": [
        ".dll",
        ".sys",
    ],
    "min_file_size_mb": 50,
    "min_age_days": 30,
    "max_workers": 8,
    "enable_duplicate_detection": True,
    "enable_folder_analysis": True,
    "top_n_files": 100,
}


class ConfigError(Exception):
    """Exception raised for configuration validation errors."""

    pass


def load_config(
    config_path: str | Path,
    scan_root_override: str | None = None,
) -> dict:
    """Load configuration from a JSON file and validate it."""
    path = Path(config_path)

    if not path.exists():
        raise ConfigError(f"Configuration file not found: {config_path}")

    try:
        with open(path, encoding="utf-8") as file:
            config = json.load(file)

    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON configuration: {e}") from e

    if scan_root_override:
        config["scan_root"] = scan_root_override

    validate_config(config)
    return config



def validate_config(config: dict) -> None:
    """Validate configuration options, raising ConfigError for invalid settings."""
    required_fields = [
        "scan_root",
        "output_csv",
        "min_file_size_mb",
        "min_age_days",
    ]

    for field in required_fields:
        if field not in config:
            raise ConfigError(f"Missing required config field: {field}")

    # Validate scan_root
    scan_root_path = Path(config["scan_root"])
    if not scan_root_path.exists():
        raise ConfigError(
            f"Config scan_root does not exist: {config['scan_root']}"
        )
    if not scan_root_path.is_dir():
        raise ConfigError(
            f"Config scan_root is not a directory: {config['scan_root']}"
        )

    # Validate min_file_size_mb
    if not isinstance(config["min_file_size_mb"], (int, float)):
        raise ConfigError("min_file_size_mb must be a number")
    if config["min_file_size_mb"] < 0:
        raise ConfigError("min_file_size_mb cannot be negative")

    # Validate min_age_days
    if not isinstance(config["min_age_days"], (int, float)):
        raise ConfigError("min_age_days must be a number")
    if config["min_age_days"] < 0:
        raise ConfigError("min_age_days cannot be negative")

    # Validate max_workers if specified
    if "max_workers" in config:
        if not isinstance(config["max_workers"], int):
            raise ConfigError("max_workers must be an integer")
        if config["max_workers"] <= 0:
            raise ConfigError("max_workers must be greater than zero")

    # Validate top_n_files if specified
    if "top_n_files" in config:
        if not isinstance(config["top_n_files"], int):
            raise ConfigError("top_n_files must be an integer")
        if config["top_n_files"] <= 0:
            raise ConfigError("top_n_files must be greater than zero")

    # Validate lists
    for list_field in ["excluded_paths", "excluded_extensions"]:
        if list_field in config:
            if not isinstance(config[list_field], list):
                raise ConfigError(f"{list_field} must be a list of strings")
            if not all(isinstance(x, str) for x in config[list_field]):
                raise ConfigError(f"All items in {list_field} must be strings")


def create_default_config(path: str | Path) -> None:
    """Create a default config.json file at the specified path."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(DEFAULT_CONFIG, file, indent=4)
