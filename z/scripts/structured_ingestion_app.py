#!/usr/bin/env python3
"""
Zuna Database CLI Sub-App

Handles all database operations:
- load: Ingest CSV files into MS SQL Server
- validate: Check data integrity and row counts
- drop: Remove all tables from a schema
- analyze: Generate JSON schema analysis with LLM insights
- report: Convert JSON analysis to Markdown report

Configuration:
    Database: raw_data_db
    Schema: seed_data_raw
    Host: 127.0.0.1:1433
    User: sa
    Password: from .env MSSQL_SA_PASSWORD

Prerequisites:
    - ODBC Driver 18 for SQL Server installed
    - MS SQL running: docker compose up -d mssql
    - LiteLLM running (for analyze): docker compose up -d litellm
"""

import asyncio
import json
import os
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import pyodbc
import typer
from dotenv import load_dotenv
from loguru import logger
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn, TimeElapsedColumn
from rich.table import Table

# Load environment variables
load_dotenv()

# Rich console for pretty output
console = Console()

# Typer sub-app
app = typer.Typer(
    name="db",
    help="""
    Database operations for Zuna.

    Commands for managing MS SQL data ingestion, validation, and analysis.

    CONFIGURATION:
      Database: raw_data_db
      Schema: seed_data_raw
      Host: 127.0.0.1:1433 (use IP, not localhost)
      Password: Set MSSQL_SA_PASSWORD in .env

    EXAMPLES:
      uv run python scripts/app.py db load
      uv run python scripts/app.py db validate
      uv run python scripts/app.py db drop --schema seed_data_raw
      uv run python scripts/app.py db analyze
      uv run python scripts/app.py db report
    """,
    no_args_is_help=True,
)

# Default configuration
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 1433
DEFAULT_DATABASE = "raw_data_db"
DEFAULT_SCHEMA = "seed_data_raw"
DEFAULT_USER = "sa"
DEFAULT_DATA_FOLDER = "seed_data"


def get_connection(
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    database: str = DEFAULT_DATABASE,
    user: str = DEFAULT_USER,
    password: Optional[str] = None,
) -> pyodbc.Connection:
    """
    Create MS SQL connection using ODBC Driver 18.

    Args:
        host: MS SQL server host (use 127.0.0.1, not localhost)
        port: MS SQL server port
        database: Database name
        user: Database user
        password: Database password (defaults to MSSQL_SA_PASSWORD env var)

    Returns:
        pyodbc.Connection object

    Raises:
        typer.Exit: If connection fails
    """
    if password is None:
        password = os.getenv("MSSQL_SA_PASSWORD")
        if not password:
            logger.error("MSSQL_SA_PASSWORD not set in environment")
            raise typer.Exit(1)

    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={host},{port};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
        f"TrustServerCertificate=yes;"
    )

    try:
        conn = pyodbc.connect(conn_str, autocommit=True)
        return conn
    except pyodbc.Error as e:
        logger.error(f"Connection failed: {e}")
        logger.info("Ensure MS SQL is running: docker compose up -d mssql")
        raise typer.Exit(1)


def get_project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).parent.parent


@app.command("load")
def load_csv(
    folder: str = typer.Option(DEFAULT_DATA_FOLDER, "--folder", "-f", help="Folder name inside data/ directory"),
    schema: str = typer.Option(DEFAULT_SCHEMA, "--schema", "-s", help="Target schema name"),
    database: str = typer.Option(DEFAULT_DATABASE, "--database", "-d", help="Target database name"),
    host: str = typer.Option(DEFAULT_HOST, "--host", "-h", help="MS SQL host (use 127.0.0.1)"),
    port: int = typer.Option(DEFAULT_PORT, "--port", "-p", help="MS SQL port"),
    batch_size: int = typer.Option(5000, "--batch-size", "-b", help="Insert batch size"),
    password: Optional[str] = typer.Option(None, "--password", envvar="MSSQL_SA_PASSWORD", help="DB password"),
):
    """
    Load CSV files into MS SQL Server.

    Reads all CSV files from data/{folder}/ and loads them into the specified schema.
    Creates schema if it doesn't exist. Drops and recreates tables.

    EXAMPLES:
        uv run python scripts/app.py db load
        uv run python scripts/app.py db load --folder seed_data --schema seed_data_raw
        uv run python scripts/app.py db load --batch-size 10000
    """
    project_root = get_project_root()
    data_dir = project_root / "data" / folder

    if not data_dir.exists():
        logger.error(f"Data directory not found: {data_dir}")
        raise typer.Exit(1)

    csv_files = list(data_dir.glob("*.csv"))
    if not csv_files:
        logger.error(f"No CSV files found in: {data_dir}")
        raise typer.Exit(1)

    logger.info(f"Database: {database} | Schema: {schema} | Host: {host}:{port}")
    logger.info(f"Data directory: {data_dir}")
    logger.info(f"Found {len(csv_files)} CSV files")

    conn = get_connection(host, port, database, password=password)
    cursor = conn.cursor()
    cursor.fast_executemany = True

    # Create schema if not exists
    cursor.execute(f"SELECT schema_name FROM INFORMATION_SCHEMA.SCHEMATA WHERE schema_name = '{schema}'")
    if not cursor.fetchone():
        cursor.execute(f"CREATE SCHEMA [{schema}]")
        logger.info(f"Created schema: {schema}")
    else:
        logger.info(f"Schema exists: {schema}")

    successful = 0
    failed = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        for csv_file in csv_files:
            table_name = csv_file.stem
            task_id = progress.add_task(f"Loading {table_name}...", total=100)

            try:
                # Read CSV
                df = pd.read_csv(csv_file)
                total_rows = len(df)
                progress.update(task_id, advance=10, description=f"[cyan]{table_name}[/] ({total_rows:,} rows)")

                # Drop existing table
                cursor.execute(f"DROP TABLE IF EXISTS [{schema}].[{table_name}]")
                progress.update(task_id, advance=10)

                # Create table - all columns as NVARCHAR for reliability
                columns_sql = []
                for col in df.columns:
                    max_len = int(df[col].astype(str).str.len().max() * 2 + 10)
                    max_len = min(max_len, 4000)
                    columns_sql.append(f"[{col}] NVARCHAR({max_len}) NULL")

                create_sql = f"CREATE TABLE [{schema}].[{table_name}] ({', '.join(columns_sql)})"
                cursor.execute(create_sql)
                progress.update(task_id, advance=10)

                # Prepare data - convert all to string, NaN to None
                df = df.astype(object).where(pd.notnull(df), None)

                # Insert data
                columns = ", ".join([f"[{col}]" for col in df.columns])
                placeholders = ", ".join(["?" for _ in df.columns])
                insert_sql = f"INSERT INTO [{schema}].[{table_name}] ({columns}) VALUES ({placeholders})"

                inserted = 0
                for i in range(0, total_rows, batch_size):
                    batch = df.iloc[i : i + batch_size]
                    data = [tuple(row) for row in batch.values]
                    cursor.executemany(insert_sql, data)
                    inserted += len(batch)
                    pct = 10 + (inserted / total_rows) * 60
                    progress.update(task_id, completed=pct)

                # Verify
                cursor.execute(f"SELECT COUNT(*) FROM [{schema}].[{table_name}]")
                count = cursor.fetchone()[0]
                progress.update(task_id, completed=100)

                if count == total_rows:
                    logger.success(f"{table_name}: {count:,} rows loaded")
                    successful += 1
                else:
                    logger.warning(f"{table_name}: Expected {total_rows:,}, got {count:,}")
                    successful += 1

            except Exception as e:
                progress.update(task_id, completed=100)
                logger.error(f"{table_name}: {e}")
                failed += 1

    cursor.close()
    conn.close()

    console.print()
    if failed == 0:
        console.print(f"[green]All {successful} tables loaded successfully![/]")
    else:
        console.print(f"[yellow]Loaded: {successful} | Failed: {failed}[/]")


@app.command("validate")
def validate_data(
    schema: str = typer.Option(DEFAULT_SCHEMA, "--schema", "-s", help="Schema to validate"),
    database: str = typer.Option(DEFAULT_DATABASE, "--database", "-d", help="Database name"),
    host: str = typer.Option(DEFAULT_HOST, "--host", "-h", help="MS SQL host"),
    port: int = typer.Option(DEFAULT_PORT, "--port", "-p", help="MS SQL port"),
    password: Optional[str] = typer.Option(None, "--password", envvar="MSSQL_SA_PASSWORD", help="DB password"),
):
    """
    Validate data in MS SQL Server.

    Shows all tables in the schema with row counts.

    EXAMPLES:
        uv run python scripts/app.py db validate
        uv run python scripts/app.py db validate --schema seed_data_raw
    """
    conn = get_connection(host, port, database, password=password)
    cursor = conn.cursor()

    cursor.execute(
        f"""
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = '{schema}' AND TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
    """
    )
    tables = [row[0] for row in cursor.fetchall()]

    if not tables:
        logger.warning(f"No tables found in schema: {schema}")
        raise typer.Exit(0)

    table = Table(title=f"Tables in {database}.{schema}")
    table.add_column("Table", style="cyan")
    table.add_column("Rows", justify="right", style="green")

    total_rows = 0
    for tbl in tables:
        cursor.execute(f"SELECT COUNT(*) FROM [{schema}].[{tbl}]")
        count = cursor.fetchone()[0]
        table.add_row(tbl, f"{count:,}")
        total_rows += count

    table.add_section()
    table.add_row("[bold]Total[/]", f"[bold]{total_rows:,}[/]")

    console.print(table)
    logger.info(f"Found {len(tables)} tables with {total_rows:,} total rows")

    cursor.close()
    conn.close()


@app.command("drop")
def drop_tables(
    schema: str = typer.Option(..., "--schema", "-s", help="Schema to drop tables from (required)"),
    database: str = typer.Option(DEFAULT_DATABASE, "--database", "-d", help="Database name"),
    host: str = typer.Option(DEFAULT_HOST, "--host", "-h", help="MS SQL host"),
    port: int = typer.Option(DEFAULT_PORT, "--port", "-p", help="MS SQL port"),
    password: Optional[str] = typer.Option(None, "--password", envvar="MSSQL_SA_PASSWORD", help="DB password"),
    force: bool = typer.Option(False, "--force", "-y", help="Skip confirmation prompt"),
):
    """
    Drop all tables from a schema.

    Removes all tables in the specified schema. Use with caution!

    EXAMPLES:
        uv run python scripts/app.py db drop --schema seed_data_raw
        uv run python scripts/app.py db drop --schema seed_data_raw --force
    """
    conn = get_connection(host, port, database, password=password)
    cursor = conn.cursor()

    # Get all tables
    cursor.execute(
        f"""
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = '{schema}' AND TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
    """
    )
    tables = [row[0] for row in cursor.fetchall()]

    if not tables:
        logger.warning(f"No tables found in schema: {schema}")
        raise typer.Exit(0)

    logger.warning(f"Found {len(tables)} tables in schema '{schema}':")
    for tbl in tables:
        console.print(f"  - {tbl}", style="yellow")

    if not force:
        confirm = typer.confirm(f"Drop all {len(tables)} tables from '{schema}'?")
        if not confirm:
            logger.info("Aborted")
            raise typer.Exit(0)

    # Drop tables
    dropped = 0
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Dropping tables...", total=len(tables))

        for tbl in tables:
            try:
                cursor.execute(f"DROP TABLE [{schema}].[{tbl}]")
                dropped += 1
                progress.update(task, advance=1, description=f"Dropped {tbl}")
            except Exception as e:
                logger.error(f"Failed to drop {tbl}: {e}")

    cursor.close()
    conn.close()

    logger.success(f"Dropped {dropped}/{len(tables)} tables from schema '{schema}'")


@app.command("analyze")
def analyze_schema(
    schema: str = typer.Option(DEFAULT_SCHEMA, "--schema", "-s", help="Schema to analyze"),
    database: str = typer.Option(DEFAULT_DATABASE, "--database", "-d", help="Database name"),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="Output JSON file path (default: data/schema_analysis/{schema}_analysis.json)"
    ),
    host: str = typer.Option(DEFAULT_HOST, "--host", "-h", help="MS SQL host"),
    port: int = typer.Option(DEFAULT_PORT, "--port", "-p", help="MS SQL port"),
    password: Optional[str] = typer.Option(None, "--password", envvar="MSSQL_SA_PASSWORD", help="DB password"),
    litellm_url: str = typer.Option("http://localhost:4000", "--litellm-url", help="LiteLLM base URL"),
    model: str = typer.Option("gpt-5-mini", "--model", "-m", help="LLM model for analysis"),
):
    """
    Analyze schema and generate JSON report.

    Connects to MS SQL, extracts schema metadata, and uses LLM for NL2SQL analysis.
    Requires LiteLLM to be running: docker compose up -d litellm

    EXAMPLES:
        uv run python scripts/app.py db analyze
        uv run python scripts/app.py db analyze --schema seed_data_raw --output analysis.json
    """
    project_root = get_project_root()

    # Default output path uses schema name
    if output is None:
        output = f"data/schema_analysis/{schema}_analysis.json"

    output_path = project_root / output

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Analyzing schema: {database}.{schema}")
    logger.info(f"Output: {output_path}")

    # Set UTF-8 encoding for Windows console (emoji support)
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

    # Import and run the analyzer
    sys.path.insert(0, str(project_root / "scripts"))

    try:
        from analyze_mssql_schema import LiteLLMClient, MSSQLSchemaAnalyzerV2

        litellm_key = os.getenv("LITELLM_MASTER_KEY")
        if not litellm_key:
            logger.error("LITELLM_MASTER_KEY not set in environment")
            raise typer.Exit(1)

        if password is None:
            password = os.getenv("MSSQL_SA_PASSWORD")

        litellm_client = LiteLLMClient(base_url=litellm_url, master_key=litellm_key, model=model)

        analyzer = MSSQLSchemaAnalyzerV2(
            host=host,
            port=port,
            database=database,
            username="sa",
            password=password,
            schema=schema,
            litellm_client=litellm_client,
        )

        with console.status("[bold green]Analyzing schema with LLM..."):
            result = asyncio.run(analyzer.analyze())

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        logger.success(f"Analysis saved to: {output_path}")
        logger.info(f"Tables analyzed: {result.get('table_count', 0)}")
        logger.info(f"Total rows: {result.get('total_rows', 0):,}")

    except ImportError as e:
        logger.error(f"Failed to import analyzer: {e}")
        raise typer.Exit(1)
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise typer.Exit(1)


@app.command("report")
def generate_report(
    schema: str = typer.Option(DEFAULT_SCHEMA, "--schema", "-s", help="Schema name (for default file paths)"),
    input_json: Optional[str] = typer.Option(
        None, "--input", "-i", help="Input JSON file path (default: data/schema_analysis/{schema}_analysis.json)"
    ),
    output_md: Optional[str] = typer.Option(
        None, "--output", "-o", help="Output Markdown file path (default: data/schema_analysis/{schema}_report.md)"
    ),
):
    """
    Generate Markdown report from JSON analysis.

    Converts the JSON schema analysis to a human-readable Markdown report.

    EXAMPLES:
        uv run python scripts/app.py db report
        uv run python scripts/app.py db report --schema zuna_seed_raw
        uv run python scripts/app.py db report --input analysis.json --output report.md
    """
    project_root = get_project_root()

    # Default paths use schema name
    if input_json is None:
        input_json = f"data/schema_analysis/{schema}_analysis.json"
    if output_md is None:
        output_md = f"data/schema_analysis/{schema}_report.md"

    input_path = project_root / input_json
    output_path = project_root / output_md

    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        logger.info("Run 'db analyze' first to generate the JSON analysis")
        raise typer.Exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Input: {input_path}")
    logger.info(f"Output: {output_path}")

    # Set UTF-8 encoding for Windows console (emoji support)
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

    sys.path.insert(0, str(project_root / "scripts"))

    try:
        from generate_schema_report import generate_markdown_report

        generate_markdown_report(str(input_path), str(output_path))
        logger.success(f"Report saved to: {output_path}")

    except ImportError as e:
        logger.error(f"Failed to import report generator: {e}")
        raise typer.Exit(1)
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        raise typer.Exit(1)


@app.command("generate")
def generate_seed_data(
    output_folder: str = typer.Option("seed_data", "--folder", "-f", help="Output folder name inside data/"),
    num_suppliers: int = typer.Option(100, "--suppliers", help="Number of suppliers"),
    num_products: int = typer.Option(1000, "--products", help="Number of products"),
    num_b2b_customers: int = typer.Option(3000, "--b2b", help="Number of B2B customers"),
    num_b2c_customers: int = typer.Option(7000, "--b2c", help="Number of B2C customers"),
    num_stores: int = typer.Option(2500, "--stores", help="Number of stores"),
    num_promotions: int = typer.Option(50, "--promotions", help="Number of promotions"),
    num_orders: int = typer.Option(15000, "--orders", help="Number of orders"),
    seed: int = typer.Option(42, "--seed", "-s", help="Random seed for reproducibility"),
):
    """
    Generate synthetic seed data (CSV files).

    Creates realistic B2B/B2C sales data with proper relationships:
    - Suppliers, Products, Customers (B2B/B2C)
    - Stores, Promotions, Orders, Order Items
    - Inventory Transactions

    EXAMPLES:
        uv run python scripts/app.py db generate
        uv run python scripts/app.py db generate --orders 5000 --b2b 1000
        uv run python scripts/app.py db generate --seed 123
    """
    # Set random seeds
    random.seed(seed)
    np.random.seed(seed)

    project_root = get_project_root()
    output_dir = project_root / "data" / output_folder
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Random seed: {seed}")

    # Date ranges
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 12, 31)

    def random_date(start, end):
        return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

    def weighted_choice(choices, weights):
        return random.choices(choices, weights=weights, k=1)[0]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        main_task = progress.add_task("Generating seed data...", total=8)

        # 1. SUPPLIERS
        progress.update(main_task, description="[cyan]Generating suppliers...")
        suppliers_data = []
        supplier_countries = ["USA", "China", "Germany", "India", "Japan", "UK", "France", "Italy", "South Korea", "Canada"]
        supplier_companies = ["Global", "International", "Worldwide", "United", "Premier", "Elite", "Superior", "Advanced", "Dynamic", "Strategic"]
        supplier_types = ["Electronics", "Textiles", "Food", "Chemicals", "Machinery", "Components"]

        for i in range(1, num_suppliers + 1):
            supplier_type = random.choice(supplier_types)
            company_prefix = random.choice(supplier_companies)
            suppliers_data.append({
                "supplier_id": f"SUP{i:05d}",
                "supplier_name": f"{company_prefix} {supplier_type} Co.",
                "contact_person": f"Contact Person {i}",
                "email": f"supplier{i}@{company_prefix.lower()}{supplier_type.lower()}.com",
                "phone": f"+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                "country": random.choice(supplier_countries),
                "rating": round(random.uniform(3.0, 5.0), 1),
                "established_year": random.randint(1980, 2020),
            })
        suppliers_df = pd.DataFrame(suppliers_data)
        suppliers_df.to_csv(output_dir / "suppliers.csv", index=False)
        progress.advance(main_task)
        logger.success(f"suppliers: {len(suppliers_df)} rows")

        # 2. PRODUCTS
        progress.update(main_task, description="[cyan]Generating products...")
        products_data = []
        categories = {
            "Electronics": ["Smartphones", "Laptops", "Tablets", "Accessories", "Wearables"],
            "Clothing": ["Men's Wear", "Women's Wear", "Kids Wear", "Footwear", "Accessories"],
            "Home & Kitchen": ["Furniture", "Appliances", "Cookware", "Decor", "Storage"],
            "Beauty": ["Skincare", "Makeup", "Haircare", "Fragrances", "Personal Care"],
            "Sports": ["Equipment", "Apparel", "Footwear", "Accessories", "Nutrition"],
            "Books": ["Fiction", "Non-Fiction", "Educational", "Comics", "Magazines"],
            "Grocery": ["Snacks", "Beverages", "Packaged Foods", "Fresh Produce", "Dairy"],
        }
        brands = {
            "Electronics": ["TechPro", "InnovateTech", "SmartGadget", "ElectroMax", "DigitalEdge"],
            "Clothing": ["FashionHub", "StyleCraft", "TrendWear", "UrbanFit", "ClassicThreads"],
            "Home & Kitchen": ["HomeComfort", "KitchenMaster", "LivingStyle", "CozySpace", "ModernHome"],
            "Beauty": ["GlowBeauty", "NaturalGlow", "BeautyEssence", "PureRadiance", "LuxeCosmetics"],
            "Sports": ["ActiveFit", "SportsPro", "AthleticEdge", "FitGear", "PerformMax"],
            "Books": ["LitHouse", "BookWorld", "ReadMore", "PageTurner", "ClassicReads"],
            "Grocery": ["FreshMart", "NatureFresh", "DailyEssentials", "PureFoods", "HealthyChoice"],
        }

        product_id = 1
        for category, subcategories in categories.items():
            category_brands = brands[category]
            num_products_in_category = num_products // len(categories)
            for _ in range(num_products_in_category):
                subcategory = random.choice(subcategories)
                brand = random.choice(category_brands)
                supplier_id = random.choice(suppliers_df["supplier_id"].tolist())
                price_ranges = {"Electronics": (50, 2000), "Clothing": (10, 200), "Home & Kitchen": (20, 500),
                               "Beauty": (5, 150), "Sports": (15, 300), "Books": (5, 50), "Grocery": (2, 50)}
                unit_price = round(random.uniform(*price_ranges.get(category, (10, 100))), 2)
                cost_price = round(unit_price * random.uniform(0.4, 0.7), 2)
                products_data.append({
                    "product_id": f"PRD{product_id:06d}",
                    "product_name": f"{brand} {subcategory} {random.randint(100, 999)}",
                    "category": category, "subcategory": subcategory, "brand": brand,
                    "sku": f"SKU-{category[:3].upper()}-{product_id:06d}",
                    "unit_price": unit_price, "cost_price": cost_price,
                    "stock_quantity": random.randint(0, 1000),
                    "supplier_id": supplier_id,
                    "weight_kg": round(random.uniform(0.1, 20.0), 2),
                    "created_date": random_date(start_date, end_date).strftime("%Y-%m-%d"),
                })
                product_id += 1
        products_df = pd.DataFrame(products_data)
        products_df.to_csv(output_dir / "products.csv", index=False)
        progress.advance(main_task)
        logger.success(f"products: {len(products_df)} rows")

        # 3. CUSTOMERS
        progress.update(main_task, description="[cyan]Generating customers...")
        customers_data = []
        cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio",
                  "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", "Columbus",
                  "Charlotte", "San Francisco", "Indianapolis", "Seattle"]
        states = ["NY", "CA", "IL", "TX", "AZ", "PA", "FL", "OH", "NC", "WA", "IN"]
        b2b_segments = ["Ecommerce", "Modern Trade", "Traditional Trade"]
        b2b_segment_weights = [0.3, 0.4, 0.3]

        for i in range(1, num_b2b_customers + 1):
            segment = weighted_choice(b2b_segments, b2b_segment_weights)
            customers_data.append({
                "customer_id": f"CUST{i:07d}", "customer_type": "B2B", "customer_segment": segment,
                "company_name": f"{random.choice(['Global', 'Prime', 'Elite', 'Metro', 'Super'])} {random.choice(['Mart', 'Store', 'Shop', 'Retail', 'Trading'])}",
                "contact_person": f"Contact {i}", "email": f"b2b.customer{i}@business.com",
                "phone": f"+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                "address": f"{random.randint(100, 9999)} {random.choice(['Main', 'Market', 'Commerce', 'Business', 'Trade'])} St",
                "city": random.choice(cities), "state": random.choice(states), "country": "USA",
                "postal_code": f"{random.randint(10000, 99999)}",
                "registration_date": random_date(start_date, end_date).strftime("%Y-%m-%d"),
                "status": weighted_choice(["Active", "Inactive"], [0.9, 0.1]),
                "credit_limit": random.randint(10000, 500000),
            })
        for i in range(num_b2b_customers + 1, num_b2b_customers + num_b2c_customers + 1):
            customers_data.append({
                "customer_id": f"CUST{i:07d}", "customer_type": "B2C", "customer_segment": "Direct Consumer",
                "company_name": None, "contact_person": f"Customer {i}", "email": f"customer{i}@email.com",
                "phone": f"+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                "address": f"{random.randint(100, 9999)} {random.choice(['Oak', 'Pine', 'Elm', 'Maple', 'Cedar'])} {random.choice(['St', 'Ave', 'Blvd', 'Dr', 'Ln'])}",
                "city": random.choice(cities), "state": random.choice(states), "country": "USA",
                "postal_code": f"{random.randint(10000, 99999)}",
                "registration_date": random_date(start_date, end_date).strftime("%Y-%m-%d"),
                "status": weighted_choice(["Active", "Inactive"], [0.95, 0.05]),
                "credit_limit": None,
            })
        customers_df = pd.DataFrame(customers_data)
        customers_df.to_csv(output_dir / "customers.csv", index=False)
        progress.advance(main_task)
        logger.success(f"customers: {len(customers_df)} rows (B2B: {num_b2b_customers}, B2C: {num_b2c_customers})")

        # 4. STORES
        progress.update(main_task, description="[cyan]Generating stores...")
        stores_data = []
        b2b_customers = customers_df[customers_df["customer_type"] == "B2B"]
        store_id = 1
        for _, customer in b2b_customers.iterrows():
            num_store = weighted_choice([1, 2, 3], [0.5, 0.3, 0.2])
            for _ in range(num_store):
                stores_data.append({
                    "store_id": f"STR{store_id:06d}", "customer_id": customer["customer_id"],
                    "store_name": f"{customer['company_name']} - {random.choice(cities)}",
                    "store_type": customer["customer_segment"],
                    "address": f"{random.randint(100, 9999)} {random.choice(['Store', 'Shop', 'Market', 'Plaza'])} St",
                    "city": random.choice(cities), "state": random.choice(states), "country": "USA",
                    "postal_code": f"{random.randint(10000, 99999)}",
                    "opening_date": random_date(datetime.strptime(customer["registration_date"], "%Y-%m-%d"), end_date).strftime("%Y-%m-%d"),
                    "size_sqft": random.randint(500, 50000), "employee_count": random.randint(5, 200),
                })
                store_id += 1
                if store_id > num_stores:
                    break
            if store_id > num_stores:
                break
        stores_df = pd.DataFrame(stores_data)
        stores_df.to_csv(output_dir / "stores.csv", index=False)
        progress.advance(main_task)
        logger.success(f"stores: {len(stores_df)} rows")

        # 5. PROMOTIONS
        progress.update(main_task, description="[cyan]Generating promotions...")
        promotions_data = []
        promotion_types = ["Percentage Discount", "Fixed Amount Off", "BOGO", "Bundle Deal", "Cashback"]
        customer_types_promo = ["B2B", "B2C", "ALL"]
        for i in range(1, num_promotions + 1):
            promo_type = random.choice(promotion_types)
            start = random_date(start_date, end_date)
            end = start + timedelta(days=random.randint(7, 90))
            discount_value = random.randint(5, 50) if promo_type in ["Percentage Discount", "Cashback"] else (random.randint(10, 500) if promo_type == "Fixed Amount Off" else 0)
            promotions_data.append({
                "promotion_id": f"PROMO{i:04d}",
                "promotion_name": f"{random.choice(['Summer', 'Winter', 'Spring', 'Fall', 'Holiday', 'Weekend', 'Flash', 'Mega'])} {promo_type} {i}",
                "promotion_type": promo_type,
                "discount_percentage": discount_value if promo_type in ["Percentage Discount", "Cashback"] else None,
                "discount_amount": discount_value if promo_type == "Fixed Amount Off" else None,
                "start_date": start.strftime("%Y-%m-%d"), "end_date": end.strftime("%Y-%m-%d"),
                "applicable_customer_type": random.choice(customer_types_promo),
                "applicable_category": random.choice([None] + list(categories.keys())),
                "min_order_amount": random.choice([0, 50, 100, 200, 500]),
                "max_discount_amount": random.choice([None, 100, 500, 1000]) if promo_type == "Percentage Discount" else None,
                "status": "Active" if start <= datetime.now() <= end else ("Expired" if end < datetime.now() else "Scheduled"),
                "usage_limit_per_customer": random.choice([None, 1, 3, 5]),
                "total_usage_limit": random.choice([None, 100, 500, 1000, 5000]),
            })
        promotions_df = pd.DataFrame(promotions_data)
        promotions_df.to_csv(output_dir / "promotions.csv", index=False)
        progress.advance(main_task)
        logger.success(f"promotions: {len(promotions_df)} rows")

        # 6. ORDERS
        progress.update(main_task, description="[cyan]Generating orders...")
        orders_data = []
        order_statuses = ["Pending", "Confirmed", "Shipped", "Delivered", "Cancelled"]
        status_weights = [0.05, 0.1, 0.15, 0.65, 0.05]
        payment_methods = ["Credit Card", "Debit Card", "Net Banking", "UPI", "Cash on Delivery", "Wire Transfer"]
        active_customers = customers_df[customers_df["status"] == "Active"]
        active_promotions = promotions_df[promotions_df["status"] == "Active"]

        for i in range(1, num_orders + 1):
            customer = active_customers.sample(1).iloc[0]
            order_date = random_date(max(start_date, datetime.strptime(customer["registration_date"], "%Y-%m-%d")), end_date)
            num_items = random.randint(5, 50) if customer["customer_type"] == "B2B" else random.randint(1, 10)
            payment_method = weighted_choice(["Wire Transfer", "Credit Card", "Net Banking"], [0.5, 0.3, 0.2]) if customer["customer_type"] == "B2B" else random.choice(payment_methods)
            applicable_promos = active_promotions[(pd.to_datetime(active_promotions["start_date"]) <= order_date) & (pd.to_datetime(active_promotions["end_date"]) >= order_date) & (active_promotions["applicable_customer_type"].isin([customer["customer_type"], "ALL"]))]
            promotion_id = applicable_promos.sample(1).iloc[0]["promotion_id"] if len(applicable_promos) > 0 and random.random() < 0.3 else None
            status = weighted_choice(order_statuses, status_weights)
            delivery_date = (order_date + timedelta(days=random.randint(2, 14))).strftime("%Y-%m-%d") if status == "Delivered" else None
            orders_data.append({
                "order_id": f"ORD{i:08d}", "customer_id": customer["customer_id"],
                "order_date": order_date.strftime("%Y-%m-%d %H:%M:%S"), "order_status": status,
                "num_items": num_items, "subtotal_amount": 0.0, "discount_amount": 0.0, "tax_amount": 0.0,
                "shipping_amount": 0.0, "final_amount": 0.0, "payment_method": payment_method,
                "shipping_address": f"{customer['address']}, {customer['city']}, {customer['state']} {customer['postal_code']}",
                "promotion_id": promotion_id, "delivery_date": delivery_date,
            })
        orders_df = pd.DataFrame(orders_data)
        progress.advance(main_task)
        logger.success(f"orders: {len(orders_df)} rows")

        # 7. ORDER ITEMS
        progress.update(main_task, description="[cyan]Generating order items...")
        order_items_data = []
        item_id = 1
        for _, order in orders_df.iterrows():
            customer_type = customers_df[customers_df["customer_id"] == order["customer_id"]].iloc[0]["customer_type"]
            selected_products = products_df.sample(n=min(order["num_items"], len(products_df)))
            subtotal = 0
            for _, product in selected_products.iterrows():
                quantity = random.randint(10, 500) if customer_type == "B2B" else random.randint(1, 5)
                line_total = product["unit_price"] * quantity
                line_discount = round(line_total * random.uniform(0, 0.15), 2)
                line_final = round(line_total - line_discount, 2)
                order_items_data.append({
                    "order_item_id": f"ITEM{item_id:010d}", "order_id": order["order_id"],
                    "product_id": product["product_id"], "quantity": quantity,
                    "unit_price": product["unit_price"], "discount_amount": line_discount,
                    "tax_amount": round(line_final * 0.08, 2), "total_amount": line_final,
                })
                subtotal += line_final
                item_id += 1
            orders_df.loc[orders_df["order_id"] == order["order_id"], "subtotal_amount"] = round(subtotal, 2)
            discount = 0
            if order["promotion_id"]:
                promo = promotions_df[promotions_df["promotion_id"] == order["promotion_id"]].iloc[0]
                if promo["discount_percentage"]:
                    discount = min(round(subtotal * (promo["discount_percentage"] / 100), 2), promo["max_discount_amount"] or float('inf'))
                elif promo["discount_amount"]:
                    discount = promo["discount_amount"]
            shipping = round(random.uniform(50, 500), 2) if customer_type == "B2B" else (round(random.uniform(5, 25), 2) if subtotal < 50 else 0)
            orders_df.loc[orders_df["order_id"] == order["order_id"], "discount_amount"] = discount
            tax = round((subtotal - discount) * 0.08, 2)
            orders_df.loc[orders_df["order_id"] == order["order_id"], "tax_amount"] = tax
            orders_df.loc[orders_df["order_id"] == order["order_id"], "shipping_amount"] = shipping
            orders_df.loc[orders_df["order_id"] == order["order_id"], "final_amount"] = round(subtotal - discount + tax + shipping, 2)

        order_items_df = pd.DataFrame(order_items_data)
        order_items_df.to_csv(output_dir / "order_items.csv", index=False)
        orders_df.to_csv(output_dir / "orders.csv", index=False)
        progress.advance(main_task)
        logger.success(f"order_items: {len(order_items_df)} rows")

        # 8. INVENTORY TRANSACTIONS
        progress.update(main_task, description="[cyan]Generating inventory transactions...")
        inventory_data = []
        for _, product in products_df.iterrows():
            inventory_data.append({
                "transaction_id": f"TXN{len(inventory_data)+1:08d}", "product_id": product["product_id"],
                "transaction_type": "IN", "quantity": product["stock_quantity"],
                "transaction_date": datetime.strptime(product["created_date"], "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S"),
                "reference_id": None, "reference_type": "Initial Stock", "notes": "Initial inventory",
            })
        for _, order_item in order_items_df.iterrows():
            order = orders_df[orders_df["order_id"] == order_item["order_id"]].iloc[0]
            inventory_data.append({
                "transaction_id": f"TXN{len(inventory_data)+1:08d}", "product_id": order_item["product_id"],
                "transaction_type": "OUT", "quantity": -order_item["quantity"],
                "transaction_date": order["order_date"], "reference_id": order_item["order_id"],
                "reference_type": "Order", "notes": f"Order fulfillment: {order_item['order_id']}",
            })
        inventory_df = pd.DataFrame(inventory_data)
        inventory_df = inventory_df.sort_values("transaction_date").reset_index(drop=True)
        inventory_df["transaction_id"] = [f"TXN{i+1:08d}" for i in range(len(inventory_df))]
        inventory_df.to_csv(output_dir / "inventory_transactions.csv", index=False)
        progress.advance(main_task)
        logger.success(f"inventory_transactions: {len(inventory_df)} rows")

    # Summary
    console.print()
    table = Table(title="Generated Seed Data Summary")
    table.add_column("File", style="cyan")
    table.add_column("Rows", justify="right", style="green")
    table.add_row("suppliers.csv", f"{len(suppliers_df):,}")
    table.add_row("products.csv", f"{len(products_df):,}")
    table.add_row("customers.csv", f"{len(customers_df):,}")
    table.add_row("stores.csv", f"{len(stores_df):,}")
    table.add_row("promotions.csv", f"{len(promotions_df):,}")
    table.add_row("orders.csv", f"{len(orders_df):,}")
    table.add_row("order_items.csv", f"{len(order_items_df):,}")
    table.add_row("inventory_transactions.csv", f"{len(inventory_df):,}")
    table.add_section()
    total = len(suppliers_df) + len(products_df) + len(customers_df) + len(stores_df) + len(promotions_df) + len(orders_df) + len(order_items_df) + len(inventory_df)
    table.add_row("[bold]Total[/]", f"[bold]{total:,}[/]")
    console.print(table)
    logger.info(f"Files saved to: {output_dir}")


if __name__ == "__main__":
    app()
