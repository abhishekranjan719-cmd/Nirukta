#!/usr/bin/env python3
"""
Zuna CLI - Main Entry Point

A unified command-line interface for Zuna data operations including:
- Structured data ingestion and management
- Unstructured data ingestion
- Graph database ingestion
- Metadata extraction (structured and unstructured)
- Schema analysis and reporting

Usage:
    uv run python scripts/app.py --help
    uv run python scripts/app.py db --help
    uv run python scripts/app.py unstructured --help
    uv run python scripts/app.py graph --help
    uv run python scripts/app.py struct-meta --help
    uv run python scripts/app.py unstruct-meta --help
"""

import sys

import typer
from loguru import logger

from structured_ingestion_app import app as db_app
from unstructured_ingestion_app import app as unstructured_app
from graph_ingestion_app import app as graph_app
from structured_metadata_extraction_app import app as struct_meta_app
from unstructured_metadata_extraction_app import app as unstruct_meta_app

# Configure loguru for console output
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    level="INFO",
    colorize=True,
)

# Main CLI app
app = typer.Typer(
    name="zuna",
    help="""
    Zuna CLI - Data Operations Tool

    Manage data ingestion, metadata extraction, and analysis operations.

    PREREQUISITES:
      - ODBC Driver 18 for SQL Server (must be installed)
      - Docker Compose services running (mssql, litellm)
      - Use 127.0.0.1 for MS SQL (NOT localhost with Docker)

    SUB-COMMANDS:
      db            Structured database operations (MS SQL)
      unstructured  Unstructured data ingestion
      graph         Graph database ingestion
      struct-meta   Structured metadata extraction
      unstruct-meta Unstructured metadata extraction
    """,
    no_args_is_help=True,
    rich_markup_mode="rich",
)

# Register sub-apps
app.add_typer(db_app, name="db", help="Structured database operations: load, validate, analyze, report, drop")
app.add_typer(unstructured_app, name="unstructured", help="Unstructured data ingestion operations")
app.add_typer(graph_app, name="graph", help="Graph database ingestion operations")
app.add_typer(struct_meta_app, name="struct-meta", help="Structured metadata extraction operations")
app.add_typer(unstruct_meta_app, name="unstruct-meta", help="Unstructured metadata extraction operations")


@app.callback()
def main_callback():
    """Zuna CLI - Data Operations Tool"""
    pass


if __name__ == "__main__":
    app()
