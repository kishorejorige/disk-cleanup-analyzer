import argparse
from pathlib import Path

from src.config_loader import ConfigError, load_config
from src.duplicate_detector import find_duplicates
from src.exporter import (
    export_duplicate_report,
    export_file_report,
    export_folder_report,
)
from src.folder_analyzer import calculate_folder_sizes
from src.html_report import generate_html_report
from src.logger import setup_logger
from src.scanner import scan_files


def run_duplicate_detection(
    config: dict,
    records: list[dict],
    output_path: str | Path,
) -> None:
    """Run duplicate file detection if enabled."""
    file_paths = [Path(record["path"]) for record in records]
    duplicates = find_duplicates(
        file_paths,
        config.get("max_workers", 8),
    )

    export_duplicate_report(
        duplicates,
        output_path,
    )



def run_folder_analysis(
    config: dict,
    output_path: str | Path,
) -> None:
    """Calculate folder sizes if enabled."""
    folder_sizes = calculate_folder_sizes(config["scan_root"])
    export_folder_report(
        folder_sizes,
        output_path,
    )



def generate_reports(
    config: dict,
    records: list[dict],
) -> None:
    """Generate CSV and HTML reports."""
    export_file_report(
        records,
        config["output_csv"],
    )

    generate_html_report(
        records,
        config.get(
            "output_html",
            "reports/disk_report.html",
        ),
    )


def main() -> None:
    """Entry point for Disk Cleanup Analyzer CLI."""
    parser = argparse.ArgumentParser(
        description="Disk Cleanup Analyzer: A read-only file scanner and storage analyzer."
    )
    parser.add_argument(
        "--config",
        default="config/config.json",
        help="Path to configuration JSON file (default: config/config.json)",
    )
    parser.add_argument(
        "--scan-root",
        help="Override the root directory to scan",
    )
    parser.add_argument(
        "--output-dir",
        help="Override the output directory for reports",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="Disk Cleanup Analyzer 0.1.0",
    )
    args = parser.parse_args()

    logger = setup_logger()

    try:
        logger.info("Application started")

        # Load configuration with scan_root override if provided
        config = load_config(args.config, scan_root_override=args.scan_root)

        # Handle output-dir override dynamically
        if args.output_dir:
            out_dir = Path(args.output_dir)
            config["output_csv"] = str(out_dir / "disk_report.csv")
            config["output_html"] = str(out_dir / "disk_report.html")
            output_duplicates = str(out_dir / "duplicates.csv")
            output_folders = str(out_dir / "folders.csv")
        else:
            output_duplicates = "reports/duplicates.csv"
            output_folders = "reports/folders.csv"

        records = scan_files(
            config,
            logger,
        )

        generate_reports(
            config,
            records,
        )

        if config.get("enable_duplicate_detection", False):
            run_duplicate_detection(
                config,
                records,
                output_duplicates,
            )
        else:
            pass

        if config.get("enable_folder_analysis", True):
            run_folder_analysis(
                config,
                output_folders,
            )
        else:
            pass

        logger.info("Application completed")

    except ConfigError as exc:
        logger.error(f"Configuration error: {exc}")
        print(f"Configuration error: {exc}")
        raise SystemExit(1) from exc
    except Exception as exc:
        logger.exception(f"Application failed: {exc}")
        raise


if __name__ == "__main__":
    main()
