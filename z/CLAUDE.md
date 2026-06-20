Zuna CLI - Data Operations Tool

Prerequisites
  ODBC Driver 18 for SQL Server installed on host
  Docker Compose services running (mssql, litellm)
  Use 127.0.0.1 for MS SQL connection (NOT localhost with Docker)
  Password from .env MSSQL_SA_PASSWORD
  uv package manager (https://docs.astral.sh/uv/)

Environment Setup

```
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies (from project root)
uv venv
uv sync
```

Database Configuration
  Database: raw_data_db
  Schema: seed_data_raw
  Host: 127.0.0.1:1433
  User: sa

Quick Start

```
docker compose up -d mssql litellm
uv run python scripts/app.py db generate
uv run python scripts/app.py db load
uv run python scripts/app.py db validate
uv run python scripts/app.py db analyze
uv run python scripts/app.py db report
```

CLI Commands

```
# Show help
uv run python scripts/app.py --help
uv run python scripts/app.py db --help
uv run python scripts/app.py unstructured --help
uv run python scripts/app.py graph --help
uv run python scripts/app.py struct-meta --help
uv run python scripts/app.py unstruct-meta --help

# Generate synthetic seed data (CSV files)
uv run python scripts/app.py db generate
uv run python scripts/app.py db generate --orders 5000 --b2b 1000
uv run python scripts/app.py db generate --seed 123

# Load CSV files to MS SQL (from data/seed_data/)
uv run python scripts/app.py db load
uv run python scripts/app.py db load --folder seed_data --schema seed_data_raw
uv run python scripts/app.py db load --batch-size 10000

# Validate data in MS SQL (show tables and row counts)
uv run python scripts/app.py db validate
uv run python scripts/app.py db validate --schema seed_data_raw

# Drop all tables from schema (requires confirmation)
uv run python scripts/app.py db drop --schema seed_data_raw
uv run python scripts/app.py db drop --schema seed_data_raw --force

# Generate JSON schema analysis (requires LiteLLM)
uv run python scripts/app.py db analyze
uv run python scripts/app.py db analyze --schema seed_data_raw --model gpt-5-mini

# Generate Markdown report from JSON
uv run python scripts/app.py db report
uv run python scripts/app.py db report --input data/schema_analysis/analysis.json --output data/schema_analysis/report.md
```

Sub-Commands
  db            Structured database operations (MS SQL)
  unstructured  Unstructured data ingestion (placeholder)
  graph         Graph database ingestion (placeholder)
  struct-meta   Structured metadata extraction (placeholder)
  unstruct-meta Unstructured metadata extraction (placeholder)

CLI Files
  scripts/app.py                                  Main CLI entry point
  scripts/structured_ingestion_app.py             db sub-app
  scripts/unstructured_ingestion_app.py           unstructured sub-app
  scripts/graph_ingestion_app.py                  graph sub-app
  scripts/structured_metadata_extraction_app.py   struct-meta sub-app
  scripts/unstructured_metadata_extraction_app.py unstruct-meta sub-app
  scripts/analyze_mssql_schema.py                 Schema analyzer module
  scripts/generate_schema_report.py               Report generator module

Output Files
  data/seed_data/*.csv                     8 CSV seed files
  data/schema_analysis/analysis.json       Schema analysis JSON
  data/schema_analysis/report.md           Markdown report

Troubleshooting
  ODBC not found: Install ODBC Driver 18 for SQL Server from Microsoft
  Connection refused: docker compose up -d mssql and wait for healthy
  LiteLLM errors: docker compose up -d litellm and wait for healthy
  Slow ingestion: Large tables (176k rows) take ~50 minutes
