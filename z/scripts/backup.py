#!/usr/bin/env python3
"""
Zuna Backup CLI - Excel to CSV Converter

Extracts all sheets from Excel files and saves them as CSV files.

Usage:
    uv run python scripts/backup.py --help
    uv run python scripts/backup.py
    uv run python scripts/backup.py --input data/zuna_seed --output data/zuna_seed
"""

from pathlib import Path

import pandas as pd
import typer
from loguru import logger
from rich.console import Console
from rich.table import Table

console = Console()

app = typer.Typer(
    name="backup",
    help="Extract Excel files to CSV format",
    no_args_is_help=False,
)


def _get_source_prefix(excel_filename: str) -> str:
    """Extract source prefix from Excel filename (b2b, ecom, pos)."""
    name_lower = excel_filename.lower()
    if "b2b" in name_lower:
        return "b2b"
    elif "ecom" in name_lower:
        return "ecom"
    elif "pos" in name_lower:
        return "pos"
    else:
        # Use first part of filename as prefix
        return excel_filename.split("_")[0].lower()


def _clean_table_name(sheet_name: str) -> str:
    """Convert sheet name to clean table name."""
    return sheet_name.strip().lower().replace(" ", "_").replace("-", "_")


@app.command()
def extract(
    input_path: Path = typer.Option(
        Path("data/zuna_seed"),
        "--input",
        "-i",
        help="Input directory containing Excel files",
    ),
    output_path: Path = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory for CSV files (default: same as input)",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed output",
    ),
):
    """Extract all sheets from Excel files and save as CSV."""
    # Use input path as output if not specified
    if output_path is None:
        output_path = input_path

    # Resolve paths relative to project root
    project_root = Path(__file__).parent.parent
    input_dir = project_root / input_path if not input_path.is_absolute() else input_path
    output_dir = project_root / output_path if not output_path.is_absolute() else output_path

    # Validate input directory
    if not input_dir.exists():
        logger.error(f"Input directory does not exist: {input_dir}")
        raise typer.Exit(1)

    # Create output directory if needed
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find all Excel files
    excel_files = list(input_dir.glob("*.xlsx")) + list(input_dir.glob("*.xls"))

    if not excel_files:
        logger.warning(f"No Excel files found in: {input_dir}")
        raise typer.Exit(0)

    logger.info(f"Found {len(excel_files)} Excel file(s) in: {input_dir}")
    logger.info(f"Output directory: {output_dir}")

    # First pass: collect all sheet names to detect duplicates
    from collections import Counter
    all_sheets = []
    excel_sheet_map = {}  # {excel_file: [(sheet_name, clean_name), ...]}

    for excel_file in excel_files:
        try:
            xlsx = pd.ExcelFile(excel_file, engine="openpyxl")
            sheets = []
            for sheet_name in xlsx.sheet_names:
                if not sheet_name.startswith("__"):
                    clean_name = _clean_table_name(sheet_name)
                    all_sheets.append(clean_name)
                    sheets.append((sheet_name, clean_name))
            excel_sheet_map[excel_file] = sheets
        except Exception as e:
            logger.error(f"Error reading {excel_file.name}: {e}")

    # Find duplicate names
    name_counts = Counter(all_sheets)
    duplicates = {name for name, count in name_counts.items() if count > 1}

    if duplicates and verbose:
        logger.info(f"Duplicate sheet names (will add source prefix): {duplicates}")

    # Second pass: extract sheets with proper naming
    results = []
    total_sheets = 0
    total_rows = 0

    for excel_file, sheets in excel_sheet_map.items():
        logger.info(f"Processing: {excel_file.name}")
        source_prefix = _get_source_prefix(excel_file.name)

        try:
            xlsx = pd.ExcelFile(excel_file, engine="openpyxl")

            for sheet_name, clean_name in sheets:
                # Read sheet
                df = pd.read_excel(xlsx, sheet_name=sheet_name)

                # Add source prefix for duplicate names
                if clean_name in duplicates:
                    table_name = f"{source_prefix}_{clean_name}"
                else:
                    table_name = clean_name

                csv_filename = f"{table_name}.csv"
                csv_path = output_dir / csv_filename

                # Save as CSV
                df.to_csv(csv_path, index=False)

                total_sheets += 1
                total_rows += len(df)

                results.append({
                    "source": source_prefix.upper(),
                    "sheet_name": sheet_name,
                    "csv_file": csv_filename,
                    "rows": len(df),
                    "columns": len(df.columns),
                })

                if verbose:
                    logger.info(f"  {sheet_name} -> {csv_filename} ({len(df)} rows)")

        except Exception as e:
            logger.error(f"Error processing {excel_file.name}: {e}")
            continue

    # Display results table
    if results:
        table = Table(title="Extracted CSV Files")
        table.add_column("Source", style="cyan")
        table.add_column("Sheet", style="green")
        table.add_column("CSV File (Table Name)", style="yellow")
        table.add_column("Rows", justify="right", style="magenta")
        table.add_column("Cols", justify="right", style="blue")

        for r in results:
            table.add_row(
                r["source"],
                r["sheet_name"],
                r["csv_file"],
                f"{r['rows']:,}",
                str(r["columns"]),
            )

        console.print(table)
        console.print()
        logger.success(f"Extracted {total_sheets} sheets with {total_rows:,} total rows")
    else:
        logger.warning("No sheets were extracted")


@app.command()
def list_files(
    input_path: Path = typer.Option(
        Path("data/zuna_seed"),
        "--input",
        "-i",
        help="Input directory containing Excel files",
    ),
):
    """List Excel files in the input directory."""
    # Resolve path relative to project root
    project_root = Path(__file__).parent.parent
    input_dir = project_root / input_path if not input_path.is_absolute() else input_path

    if not input_dir.exists():
        logger.error(f"Directory does not exist: {input_dir}")
        raise typer.Exit(1)

    excel_files = list(input_dir.glob("*.xlsx")) + list(input_dir.glob("*.xls"))

    if not excel_files:
        logger.warning(f"No Excel files found in: {input_dir}")
        raise typer.Exit(0)

    table = Table(title=f"Excel Files in {input_dir}")
    table.add_column("File", style="cyan")
    table.add_column("Size", justify="right", style="green")
    table.add_column("Sheets", justify="right", style="yellow")

    for excel_file in excel_files:
        try:
            xlsx = pd.ExcelFile(excel_file, engine="openpyxl")
            sheet_count = len(xlsx.sheet_names)
            size_mb = excel_file.stat().st_size / (1024 * 1024)
            table.add_row(excel_file.name, f"{size_mb:.2f} MB", str(sheet_count))
        except Exception as e:
            table.add_row(excel_file.name, "Error", str(e))

    console.print(table)


if __name__ == "__main__":
    app()
