# Zuna CLI - Data Operations Tool

A unified command-line interface for data ingestion, metadata extraction, and analysis operations.

## Prerequisites

- **ODBC Driver 18 for SQL Server** - Must be installed on host machine
- **Docker Compose** - MS SQL and LiteLLM services must be running
- **Python 3.12+** - Via uv virtual environment
- **uv** - Python package manager (https://docs.astral.sh/uv/)

## Environment Setup

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies (from project root)
uv venv
uv sync
```

## Quick Start

```bash
# Start required services
docker compose up -d mssql litellm

# Generate seed data
uv run python scripts/app.py db generate

# Load data to MS SQL
uv run python scripts/app.py db load

# Validate data
uv run python scripts/app.py db validate

# Analyze schema (requires LiteLLM)
uv run python scripts/app.py db analyze

# Generate markdown report
uv run python scripts/app.py db report
```

## CLI Structure

```
scripts/
  app.py                                  Main CLI entry point
  structured_ingestion_app.py             Structured DB sub-app (db)
  unstructured_ingestion_app.py           Unstructured ingestion sub-app (unstructured)
  graph_ingestion_app.py                  Graph DB sub-app (graph)
  structured_metadata_extraction_app.py   Structured metadata sub-app (struct-meta)
  unstructured_metadata_extraction_app.py Unstructured metadata sub-app (unstruct-meta)
  analyze_mssql_schema.py                 Schema analyzer module
  generate_schema_report.py               Report generator module
```

## Sub-Commands Overview

| Command | Description |
|---------|-------------|
| `db` | Structured database operations (MS SQL) |
| `unstructured` | Unstructured data ingestion |
| `graph` | Graph database ingestion |
| `struct-meta` | Structured metadata extraction |
| `unstruct-meta` | Unstructured metadata extraction |

## Commands

### `db generate`
Generate synthetic B2B/B2C sales data as CSV files.

```bash
uv run python scripts/app.py db generate
uv run python scripts/app.py db generate --orders 5000 --b2b 1000
uv run python scripts/app.py db generate --seed 123
```

Options:
- `--folder` - Output folder name inside data/ (default: seed_data)
- `--suppliers` - Number of suppliers (default: 100)
- `--products` - Number of products (default: 1000)
- `--b2b` - Number of B2B customers (default: 3000)
- `--b2c` - Number of B2C customers (default: 7000)
- `--stores` - Number of stores (default: 2500)
- `--promotions` - Number of promotions (default: 50)
- `--orders` - Number of orders (default: 15000)
- `--seed` - Random seed for reproducibility (default: 42)

### `db load`
Load CSV files into MS SQL Server.

```bash
uv run python scripts/app.py db load
uv run python scripts/app.py db load --folder seed_data --schema seed_data_raw
uv run python scripts/app.py db load --batch-size 10000
```

Options:
- `--folder` - Folder name inside data/ directory (default: seed_data)
- `--schema` - Target schema name (default: seed_data_raw)
- `--database` - Target database name (default: raw_data_db)
- `--host` - MS SQL host (default: 127.0.0.1)
- `--port` - MS SQL port (default: 1433)
- `--batch-size` - Insert batch size (default: 5000)

### `db validate`
Validate data in MS SQL Server - shows tables and row counts.

```bash
uv run python scripts/app.py db validate
uv run python scripts/app.py db validate --schema seed_data_raw
```

### `db drop`
Drop all tables from a schema.

```bash
uv run python scripts/app.py db drop --schema seed_data_raw
uv run python scripts/app.py db drop --schema seed_data_raw --force
```

Options:
- `--schema` - Schema to drop tables from (required)
- `--force` - Skip confirmation prompt

### `db analyze`
Analyze schema and generate JSON report with LLM insights.

```bash
uv run python scripts/app.py db analyze
uv run python scripts/app.py db analyze --schema seed_data_raw
uv run python scripts/app.py db analyze --model gpt-5-mini
```

Options:
- `--schema` - Schema to analyze (default: seed_data_raw)
- `--output` - Output JSON file path (default: data/schema_analysis/analysis.json)
- `--model` - LLM model for analysis (default: gpt-5-mini)
- `--litellm-url` - LiteLLM base URL (default: http://localhost:4000)

### `db report`
Generate Markdown report from JSON analysis.

```bash
uv run python scripts/app.py db report
uv run python scripts/app.py db report --input analysis.json --output report.md
```

Options:
- `--input` - Input JSON file path (default: data/schema_analysis/analysis.json)
- `--output` - Output Markdown file path (default: data/schema_analysis/report.md)

## Database Configuration

| Setting | Value |
|---------|-------|
| Database | raw_data_db |
| Schema | seed_data_raw |
| Host | 127.0.0.1 |
| Port | 1433 |
| User | sa |
| Password | MSSQL_SA_PASSWORD env var |

## Output Files

| File | Description |
|------|-------------|
| data/seed_data/*.csv | 8 CSV seed files |
| data/schema_analysis/analysis.json | Schema analysis with LLM insights |
| data/schema_analysis/report.md | Human-readable Markdown report |

## Generated Data Structure

The seed data generator creates realistic B2B/B2C sales data:

- **suppliers.csv** - Supplier master data
- **products.csv** - Product catalog with categories
- **customers.csv** - B2B and B2C customers
- **stores.csv** - B2B customer store locations
- **promotions.csv** - Promotional campaigns
- **orders.csv** - Order headers
- **order_items.csv** - Order line items
- **inventory_transactions.csv** - Inventory movements

## Troubleshooting

| Issue | Solution |
|-------|----------|
| ODBC not found | Install "ODBC Driver 18 for SQL Server" from Microsoft |
| Connection refused | Run `docker compose up -d mssql` and wait for healthy status |
| LiteLLM errors | Run `docker compose up -d litellm` and wait for healthy status |
| Slow ingestion | Large tables (176k rows) take ~50 minutes |
