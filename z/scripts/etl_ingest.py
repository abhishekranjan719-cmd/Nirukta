#!/usr/bin/env python3
"""
Zuna ETL Ingestion Script

This script performs ETL (Extract, Transform, Load) operations on the seed data:
1. Extract: Read CSV files from data/zuna_seed
2. Transform: Fix data types, clean column names, handle nulls
3. Load: Create schema with proper PK/FK constraints and ingest data

Key transformations:
- Convert numeric strings to proper numeric types (DECIMAL, INT)
- Convert date strings to proper DATE/DATETIME types
- Remove "Unnamed: X" columns (100% NULL)
- Rename columns with spaces to use underscores
- Add PRIMARY KEY constraints
- Add FOREIGN KEY relationships

Usage:
    uv run python scripts/etl_ingest.py --schema zuna_etl
    uv run python scripts/etl_ingest.py --schema zuna_etl --drop-existing
"""

import os
import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pyodbc
import typer
from loguru import logger
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Force ASCII-compatible output for Windows console
console = Console(force_terminal=True, legacy_windows=True)
app = typer.Typer(name="etl-ingest", help="ETL ingestion with data quality fixes")

# Database configuration
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 1433
DEFAULT_DATABASE = "raw_data_db"
DEFAULT_SCHEMA = "zuna_etl"

# =============================================================================
# PRIMARY KEY DEFINITIONS
# =============================================================================
# Maps table names to their primary key column(s)
PRIMARY_KEYS: dict[str, list[str]] = {
    # B2B tables
    "b2b_contracts": ["contract_id"],
    "b2b_credit_notes": ["credit_note_id"],
    "b2b_customer_addresses": ["address_id"],
    "b2b_customers": ["customer_id"],
    "b2b_dispatches": ["dispatch_id"],
    "b2b_events_stream": ["event_id"],
    "b2b_invoices": ["invoice_id"],
    "b2b_kpi_daily_snapshots": ["snapshot_id"],
    "b2b_order_allocations": ["allocation_id"],
    "b2b_order_events": ["event_id"],
    "b2b_order_lines": ["order_line_id"],
    "b2b_orders": ["order_id"],
    "b2b_payments": ["payment_id"],
    "b2b_picking_batches": ["batch_id"],
    "b2b_portal_api_clients": ["client_id"],
    "b2b_price_list": ["price_list_id"],
    "b2b_product_sales": ["sku"],
    "b2b_product_wise_sales": ["sku", "date"],
    "b2b_products": ["sku"],
    "b2b_quality_inspections": ["inspection_id"],
    "b2b_returns": ["return_id"],
    "b2b_sales_agents": ["agent_id"],
    "b2b_sales_daily": ["date", "channel"],
    "b2b_sales_monthly": ["month", "year", "channel"],
    "b2b_sales_yearly": ["year", "channel"],
    "b2b_shipment_tracking_events": ["event_id"],
    "b2b_vendor_partners": ["vendor_id"],
    # Ecom tables
    "ecom_ab_test": ["test_id"],
    "ecom_acquisition_agents": ["agent_id"],
    "ecom_activity_log": ["activity_id"],
    "ecom_browsing_history": ["browse_id"],
    "ecom_cart_items": ["cart_item_id"],
    "ecom_carts": ["cart_id"],
    "ecom_coupon_usage": ["usage_id"],
    "ecom_coupons": ["coupon_id"],
    "ecom_customer_addresses": ["address_id"],
    "ecom_customer_segmentation": ["customer_id"],
    "ecom_customers": ["customer_id"],
    "ecom_frequently_bought": ["pair_id"],
    "ecom_notifications": ["notification_id"],
    "ecom_orders": ["order_id"],
    "ecom_payment_status_log": ["log_id"],
    "ecom_payments": ["payment_id"],
    "ecom_product_events": ["event_id"],
    "ecom_product_wise_sales": ["sku", "date"],
    "ecom_ratings_summary": ["sku"],
    "ecom_refunds": ["refund_id"],
    "ecom_return_items": ["return_item_id"],
    "ecom_reviews": ["review_id"],
    "ecom_sales_daily": ["date", "channel"],
    "ecom_sales_monthly": ["month", "year", "channel"],
    "ecom_sales_yearly": ["year", "channel"],
    "ecom_search_keywords": ["keyword_id"],
    "ecom_ticket": ["ticket_id"],
    "ecom_ticket_messages": ["message_id"],
    "ecom_vendors": ["vendor_id"],
    "ecom_wishlist": ["wishlist_item_id"],
    # POS tables
    "pos_daily_sales_summary": ["summary_id"],
    "pos_inventory_adjustments": ["adjustment_id"],
    "pos_loyalty_redemptions": ["redemption_id"],
    "pos_product_wise_sales": ["sku", "date"],
    "pos_products": ["sku"],
    "pos_products_sales": ["sku"],
    "pos_returns": ["return_id"],
    "pos_sales_daily": ["date", "store_id"],
    "pos_sales_monthly": ["month", "year", "store_id"],
    "pos_sales_yearly": ["year", "store_id"],
    "pos_shift_closures": ["closure_id"],
    "pos_stores": ["store_id"],
    "pos_sync_log": ["sync_id"],
    "pos_terminals": ["terminal_id"],
    "pos_transaction_lines": ["line_id"],
    "pos_transactions": ["txn_id"],
    "pos_users": ["user_id"],
    "pos_vendors": ["vendor_id"],
    # Common tables
    "delivery_slots": ["slot_id"],
    "delivery_status": ["status_id"],
    "inventory_items": ["item_id"],
    "order_items": ["order_item_id"],
    "product_inventory": ["inventory_id"],
    "product_pricing": ["pricing_id"],
    "product_sales": ["sku"],
    "product_variants": ["variant_id"],
    "products": ["sku"],
    "returns": ["return_id"],
    "shipments": ["shipment_id"],
}

# =============================================================================
# FOREIGN KEY DEFINITIONS
# =============================================================================
# Maps (table, column) to (referenced_table, referenced_column)
FOREIGN_KEYS: dict[str, list[tuple[str, str, str]]] = {
    # B2B relationships
    "b2b_contracts": [("customer_id", "b2b_customers", "customer_id")],
    "b2b_credit_notes": [("invoice_id", "b2b_invoices", "invoice_id")],
    "b2b_customer_addresses": [("customer_id", "b2b_customers", "customer_id")],
    "b2b_dispatches": [("order_id", "b2b_orders", "order_id")],
    "b2b_invoices": [
        ("order_id", "b2b_orders", "order_id"),
        ("customer_id", "b2b_customers", "customer_id"),
    ],
    "b2b_order_allocations": [("order_id", "b2b_orders", "order_id")],
    "b2b_order_events": [("order_id", "b2b_orders", "order_id")],
    "b2b_order_lines": [
        ("order_id", "b2b_orders", "order_id"),
        ("sku", "b2b_products", "sku"),
    ],
    "b2b_orders": [("customer_id", "b2b_customers", "customer_id")],
    "b2b_payments": [("invoice_id", "b2b_invoices", "invoice_id")],
    "b2b_price_list": [
        ("customer_id", "b2b_customers", "customer_id"),
        ("sku", "b2b_products", "sku"),
    ],
    "b2b_returns": [("order_id", "b2b_orders", "order_id")],
    "b2b_shipment_tracking_events": [("dispatch_id", "b2b_dispatches", "dispatch_id")],
    # Ecom relationships
    "ecom_browsing_history": [("customer_id", "ecom_customers", "customer_id")],
    "ecom_cart_items": [("cart_id", "ecom_carts", "cart_id")],
    "ecom_carts": [("customer_id", "ecom_customers", "customer_id")],
    "ecom_coupon_usage": [
        ("order_id", "ecom_orders", "order_id"),
        ("coupon_id", "ecom_coupons", "coupon_id"),
    ],
    "ecom_customer_addresses": [("customer_id", "ecom_customers", "customer_id")],
    "ecom_customer_segmentation": [("customer_id", "ecom_customers", "customer_id")],
    "ecom_notifications": [("customer_id", "ecom_customers", "customer_id")],
    "ecom_orders": [("customer_id", "ecom_customers", "customer_id")],
    "ecom_payments": [("order_id", "ecom_orders", "order_id")],
    "ecom_refunds": [("order_id", "ecom_orders", "order_id")],
    "ecom_reviews": [("customer_id", "ecom_customers", "customer_id")],
    "ecom_ticket": [
        ("customer_id", "ecom_customers", "customer_id"),
        ("order_id", "ecom_orders", "order_id"),
    ],
    "ecom_ticket_messages": [("ticket_id", "ecom_ticket", "ticket_id")],
    "ecom_wishlist": [("customer_id", "ecom_customers", "customer_id")],
    # POS relationships
    "pos_inventory_adjustments": [("sku", "pos_products", "sku")],
    "pos_shift_closures": [("terminal_id", "pos_terminals", "terminal_id")],
    "pos_terminals": [("store_id", "pos_stores", "store_id")],
    "pos_transaction_lines": [("txn_id", "pos_transactions", "txn_id")],
    "pos_transactions": [("terminal_id", "pos_terminals", "terminal_id")],
    # Common relationships
    "order_items": [("order_id", "ecom_orders", "order_id")],
    "product_variants": [("sku", "products", "sku")],
    "product_pricing": [("sku", "products", "sku")],
    "product_inventory": [("sku", "products", "sku")],
    "returns": [("order_id", "ecom_orders", "order_id")],
    "shipments": [("order_id", "ecom_orders", "order_id")],
    "delivery_status": [("order_id", "ecom_orders", "order_id")],
}

# =============================================================================
# COLUMN TYPE MAPPINGS
# =============================================================================
# Columns that should be converted to specific types
NUMERIC_COLUMNS = {
    # Amount/money columns
    "amount", "gross_amount", "tax_amount", "discount_amount", "net_amount",
    "refund_amount", "line_total", "total_amount", "unit_price", "price_per_unit",
    "pos_price", "mrp", "cost_price", "selling_price", "base_price",
    "txn_total", "tax_total", "discount_total", "total_sales", "total_tax",
    "total_refunds", "avg_txn_value", "counted_cash", "gross_sales", "net_sales",
    # Quantity columns
    "qty", "qty_kg", "quantity", "total_qty_kg", "stock_qty", "total_kg",
    "min_order_qty", "reorder_level", "total_stock_units", "current_stock",
    # Count columns
    "total_orders", "total_bills", "total_txns", "total_customers", "retry_count",
    "view_count", "click_count", "search_count", "usage_count",
    # Other numeric
    "discount_pct", "tax_pct", "discount_percent", "latitude", "longitude",
    "min_monthly_volume", "gross_weight_kg", "net_weight_kg", "weight_kg",
}

DATE_COLUMNS = {
    "date", "created_at", "updated_at", "start_date", "end_date", "order_date",
    "delivery_date", "dispatch_date", "invoice_date", "payment_date", "join_date",
    "event_ts", "issued_at", "approved_at", "processed_at", "last_login",
    "expiry_date", "valid_from", "valid_to", "shipped_at", "delivered_at",
}

# Columns to drop (100% NULL or meaningless)
DROP_COLUMN_PATTERNS = [
    r"^Unnamed:\s*\d+$",  # Unnamed: 0, Unnamed: 1, etc.
]


def get_project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).parent.parent


def get_connection_string(host: str, port: int, database: str, password: str) -> str:
    """Build ODBC connection string."""
    return (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={host},{port};"
        f"DATABASE={database};"
        f"UID=sa;"
        f"PWD={password};"
        f"TrustServerCertificate=yes;"
        f"Connection Timeout=30;"
    )


def clean_column_name(col: str) -> str:
    """Clean column name: lowercase, replace spaces with underscores."""
    # Replace spaces with underscores
    col = col.strip().replace(" ", "_").replace("-", "_")
    # Remove special characters except underscores
    col = re.sub(r"[^a-zA-Z0-9_]", "", col)
    # Lowercase
    col = col.lower()
    return col


def should_drop_column(col: str) -> bool:
    """Check if column should be dropped."""
    for pattern in DROP_COLUMN_PATTERNS:
        if re.match(pattern, col, re.IGNORECASE):
            return True
    return False


def infer_sql_type(col_name: str, dtype: str, sample_values: pd.Series) -> str:
    """Infer SQL Server data type from column name and pandas dtype."""
    col_lower = col_name.lower()

    # Check for ID columns - use NVARCHAR for string IDs
    if col_lower.endswith("_id") or col_lower == "sku":
        max_len = sample_values.astype(str).str.len().max()
        max_len = max(50, int(max_len * 1.5)) if pd.notna(max_len) else 100
        return f"NVARCHAR({max_len})"

    # Check for date columns
    if col_lower in DATE_COLUMNS or col_lower.endswith("_at") or col_lower.endswith("_date"):
        return "DATETIME2"

    # Check for numeric columns
    if col_lower in NUMERIC_COLUMNS:
        return "DECIMAL(18,4)"

    # Check for boolean columns
    if col_lower.endswith("_flag") or col_lower.startswith("is_"):
        return "BIT"

    # Check pandas dtype
    if dtype.startswith("int"):
        return "BIGINT"
    elif dtype.startswith("float"):
        return "DECIMAL(18,4)"
    elif dtype == "bool":
        return "BIT"
    elif dtype == "datetime64[ns]":
        return "DATETIME2"

    # Default to NVARCHAR
    max_len = sample_values.astype(str).str.len().max()
    max_len = max(50, int(max_len * 1.5)) if pd.notna(max_len) else 255
    max_len = min(max_len, 4000)  # SQL Server NVARCHAR limit
    return f"NVARCHAR({max_len})"


def transform_dataframe(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    """Apply transformations to clean and fix data types."""
    # 1. Drop unnamed columns
    cols_to_drop = [col for col in df.columns if should_drop_column(col)]
    if cols_to_drop:
        logger.info(f"  Dropping columns: {cols_to_drop}")
        df = df.drop(columns=cols_to_drop)

    # 2. Clean column names
    df.columns = [clean_column_name(col) for col in df.columns]

    # 2.5. Handle NULL values in PK columns - drop rows with NULL PKs
    pk_cols = PRIMARY_KEYS.get(table_name, [])
    if pk_cols:
        existing_pk_cols = [col for col in pk_cols if col in df.columns]
        if existing_pk_cols:
            original_len = len(df)
            df = df.dropna(subset=existing_pk_cols)
            dropped = original_len - len(df)
            if dropped > 0:
                logger.warning(f"  Dropped {dropped} rows with NULL primary key values")

            # 2.6. Remove duplicate PK values (keep first occurrence)
            before_dedup = len(df)
            df = df.drop_duplicates(subset=existing_pk_cols, keep="first")
            dupes_removed = before_dedup - len(df)
            if dupes_removed > 0:
                logger.warning(f"  Removed {dupes_removed} duplicate primary key rows")

    # 3. Convert date columns
    for col in df.columns:
        col_lower = col.lower()
        if col_lower in DATE_COLUMNS or col_lower.endswith("_at") or col_lower.endswith("_date"):
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
            except Exception:
                pass

    # 4. Convert numeric columns
    for col in df.columns:
        col_lower = col.lower()
        if col_lower in NUMERIC_COLUMNS:
            try:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            except Exception:
                pass

    # 5. Convert boolean columns
    for col in df.columns:
        col_lower = col.lower()
        if col_lower.endswith("_flag") or col_lower.startswith("is_"):
            try:
                # Handle True/False strings
                df[col] = df[col].map(
                    lambda x: True if str(x).lower() in ("true", "1", "yes") else
                    (False if str(x).lower() in ("false", "0", "no") else None)
                )
            except Exception:
                pass

    # 6. Replace NaN/inf values with None for SQL Server compatibility
    for col in df.columns:
        if df[col].dtype in ['float64', 'float32', 'int64', 'int32']:
            # Replace inf/-inf with NaN, then NaN with None
            df[col] = df[col].replace([np.inf, -np.inf], np.nan)
        # Replace all NaN with None (becomes SQL NULL)
        df[col] = df[col].where(pd.notna(df[col]), None)

    return df


def generate_create_table_sql(
    table_name: str,
    df: pd.DataFrame,
    schema: str,
) -> str:
    """Generate CREATE TABLE SQL with proper types and PK."""
    # Get PK columns for this table (lowercase for comparison)
    pk_cols = PRIMARY_KEYS.get(table_name, [])
    pk_cols_lower = [col.lower() for col in pk_cols]

    columns = []
    for col in df.columns:
        sql_type = infer_sql_type(col, str(df[col].dtype), df[col])
        # PK columns must be NOT NULL
        nullable = "NULL" if col.lower() not in pk_cols_lower else "NOT NULL"
        columns.append(f"    [{col}] {sql_type} {nullable}")

    # Add primary key constraint if defined
    pk_constraint = ""
    if pk_cols:
        # Check if PK columns exist in dataframe
        existing_pk_cols = [col for col in pk_cols if col in df.columns]
        if existing_pk_cols:
            pk_col_list = ", ".join([f"[{col}]" for col in existing_pk_cols])
            pk_constraint = f",\n    CONSTRAINT [PK_{table_name}] PRIMARY KEY ({pk_col_list})"

    columns_sql = ",\n".join(columns)
    sql = f"""CREATE TABLE [{schema}].[{table_name}] (
{columns_sql}{pk_constraint}
);"""
    return sql


def generate_foreign_key_sql(table_name: str, schema: str) -> list[str]:
    """Generate ALTER TABLE statements for foreign keys."""
    fk_defs = FOREIGN_KEYS.get(table_name, [])
    statements = []
    for fk_col, ref_table, ref_col in fk_defs:
        fk_name = f"FK_{table_name}_{fk_col}"
        sql = f"""ALTER TABLE [{schema}].[{table_name}]
ADD CONSTRAINT [{fk_name}]
FOREIGN KEY ([{fk_col}]) REFERENCES [{schema}].[{ref_table}]([{ref_col}]);"""
        statements.append(sql)
    return statements


def drop_schema_tables(cursor: Any, schema: str) -> None:
    """Drop all tables in schema."""
    # First drop all foreign keys
    cursor.execute(f"""
        SELECT
            fk.name AS fk_name,
            OBJECT_NAME(fk.parent_object_id) AS table_name
        FROM sys.foreign_keys fk
        JOIN sys.tables t ON fk.parent_object_id = t.object_id
        JOIN sys.schemas s ON t.schema_id = s.schema_id
        WHERE s.name = '{schema}'
    """)
    fks = cursor.fetchall()
    for fk_name, table_name in fks:
        cursor.execute(f"ALTER TABLE [{schema}].[{table_name}] DROP CONSTRAINT [{fk_name}]")
        logger.info(f"  Dropped FK: {fk_name}")

    # Then drop tables
    cursor.execute(f"""
        SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = '{schema}' AND TABLE_TYPE = 'BASE TABLE'
    """)
    tables = [row[0] for row in cursor.fetchall()]
    for table in tables:
        cursor.execute(f"DROP TABLE [{schema}].[{table}]")
        logger.info(f"  Dropped table: {table}")


def create_schema_if_not_exists(cursor: Any, schema: str) -> None:
    """Create schema if it doesn't exist."""
    cursor.execute(f"""
        IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = '{schema}')
        BEGIN
            EXEC('CREATE SCHEMA [{schema}]')
        END
    """)


def insert_dataframe(
    cursor: Any,
    df: pd.DataFrame,
    schema: str,
    table_name: str,
    batch_size: int = 1000,
) -> int:
    """Insert dataframe into table using batched inserts."""
    if df.empty:
        return 0

    columns = df.columns.tolist()
    col_list = ", ".join([f"[{col}]" for col in columns])
    placeholders = ", ".join(["?" for _ in columns])
    insert_sql = f"INSERT INTO [{schema}].[{table_name}] ({col_list}) VALUES ({placeholders})"

    # Convert dataframe to list of tuples with proper None handling
    def clean_value(val):
        """Convert pandas NA/NaN/NaT to Python None."""
        if val is None:
            return None
        if pd.isna(val):
            return None
        if isinstance(val, float) and (np.isnan(val) or np.isinf(val)):
            return None
        return val

    rows_inserted = 0
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i : i + batch_size]
        values = [tuple(clean_value(v) for v in row) for row in batch.values]
        cursor.executemany(insert_sql, values)
        rows_inserted += len(batch)

    return rows_inserted


@app.command()
def ingest(
    input_folder: str = typer.Option("data/zuna_seed", "--input", "-i", help="Input folder with CSVs"),
    schema: str = typer.Option(DEFAULT_SCHEMA, "--schema", "-s", help="Target schema name"),
    database: str = typer.Option(DEFAULT_DATABASE, "--database", "-d", help="Database name"),
    host: str = typer.Option(DEFAULT_HOST, "--host", "-h", help="MS SQL host"),
    port: int = typer.Option(DEFAULT_PORT, "--port", "-p", help="MS SQL port"),
    password: str | None = typer.Option(None, "--password", envvar="MSSQL_SA_PASSWORD", help="DB password"),
    drop_existing: bool = typer.Option(False, "--drop-existing", help="Drop existing tables first"),
    skip_fk: bool = typer.Option(False, "--skip-fk", help="Skip foreign key creation"),
    batch_size: int = typer.Option(1000, "--batch-size", help="Batch size for inserts"),
):
    """
    ETL ingest: Extract CSVs, Transform data, Load to MS SQL with PK/FK.

    EXAMPLES:
        uv run python scripts/etl_ingest.py --schema zuna_etl
        uv run python scripts/etl_ingest.py --schema zuna_etl --drop-existing
        uv run python scripts/etl_ingest.py --schema zuna_etl --skip-fk
    """
    if not password:
        logger.error("Password required. Set MSSQL_SA_PASSWORD env var or use --password")
        raise typer.Exit(1)

    project_root = get_project_root()
    input_path = project_root / input_folder

    if not input_path.exists():
        logger.error(f"Input folder not found: {input_path}")
        raise typer.Exit(1)

    csv_files = sorted(input_path.glob("*.csv"))
    if not csv_files:
        logger.error(f"No CSV files found in: {input_path}")
        raise typer.Exit(1)

    logger.info(f"Found {len(csv_files)} CSV files in {input_path}")

    # Connect to database
    conn_str = get_connection_string(host, port, database, password)
    try:
        conn = pyodbc.connect(conn_str)
        conn.autocommit = False
        cursor = conn.cursor()
        logger.success(f"Connected to {database}")
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        raise typer.Exit(1)

    try:
        # Create schema
        create_schema_if_not_exists(cursor, schema)
        conn.commit()
        logger.info(f"Schema [{schema}] ready")

        # Drop existing tables if requested
        if drop_existing:
            logger.info("Dropping existing tables...")
            drop_schema_tables(cursor, schema)
            conn.commit()

        # Track table creation order for FK dependencies
        created_tables: set[str] = set()
        fk_statements: list[tuple[str, str]] = []  # (table, sql)

        console.print(f"\n[bold]Processing {len(csv_files)} CSV files...[/bold]\n")

        # Phase 1: Create tables and load data
        with Progress(
            SpinnerColumn(spinner_name="line"),  # ASCII-compatible spinner
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            for csv_file in csv_files:
                table_name = csv_file.stem
                task = progress.add_task(f"Processing {table_name}...", total=None)

                # Read CSV
                df = pd.read_csv(csv_file, encoding="utf-8")
                original_rows = len(df)
                original_cols = len(df.columns)

                # Transform
                df = transform_dataframe(df, table_name)

                # Check if table exists
                cursor.execute(f"""
                    SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{table_name}'
                """)
                table_exists = cursor.fetchone()[0] > 0

                if table_exists and not drop_existing:
                    # Table exists, just insert
                    rows = insert_dataframe(cursor, df, schema, table_name, batch_size)
                    conn.commit()
                    logger.info(f"  {table_name}: Inserted {rows} rows (table existed)")
                else:
                    # Create table
                    create_sql = generate_create_table_sql(table_name, df, schema)
                    cursor.execute(create_sql)
                    conn.commit()

                    # Insert data
                    rows = insert_dataframe(cursor, df, schema, table_name, batch_size)
                    conn.commit()

                    created_tables.add(table_name)
                    logger.info(
                        f"  {table_name}: {original_cols} cols → {len(df.columns)} cols, "
                        f"{original_rows} rows loaded"
                    )

                # Collect FK statements for later
                if not skip_fk:
                    for fk_sql in generate_foreign_key_sql(table_name, schema):
                        fk_statements.append((table_name, fk_sql))

                progress.remove_task(task)

        # Phase 2: Add foreign keys (after all tables exist)
        if fk_statements and not skip_fk:
            console.print(f"\n[bold]Adding {len(fk_statements)} foreign key constraints...[/bold]\n")
            fk_success = 0
            fk_failed = 0
            for table_name, fk_sql in fk_statements:
                try:
                    cursor.execute(fk_sql)
                    conn.commit()
                    fk_success += 1
                except Exception as e:
                    # FK might fail if referenced table doesn't exist or data mismatch
                    logger.warning(f"  FK failed for {table_name}: {e}")
                    fk_failed += 1
                    conn.rollback()

            logger.info(f"Foreign keys: {fk_success} added, {fk_failed} failed")

        # Summary
        console.print(f"\n[bold green]ETL Complete![/bold green]")
        console.print(f"  Schema: [{schema}]")
        console.print(f"  Tables created: {len(created_tables)}")
        console.print(f"  Total CSV files processed: {len(csv_files)}")

    except Exception as e:
        logger.error(f"ETL failed: {e}")
        conn.rollback()
        raise typer.Exit(1)
    finally:
        cursor.close()
        conn.close()


@app.command()
def validate(
    schema: str = typer.Option(DEFAULT_SCHEMA, "--schema", "-s", help="Schema to validate"),
    database: str = typer.Option(DEFAULT_DATABASE, "--database", "-d", help="Database name"),
    host: str = typer.Option(DEFAULT_HOST, "--host", "-h", help="MS SQL host"),
    port: int = typer.Option(DEFAULT_PORT, "--port", "-p", help="MS SQL port"),
    password: str | None = typer.Option(None, "--password", envvar="MSSQL_SA_PASSWORD", help="DB password"),
):
    """Validate ETL results: show tables, row counts, PK/FK status."""
    if not password:
        logger.error("Password required. Set MSSQL_SA_PASSWORD env var or use --password")
        raise typer.Exit(1)

    conn_str = get_connection_string(host, port, database, password)
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        raise typer.Exit(1)

    try:
        # Get tables
        cursor.execute(f"""
            SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = '{schema}' AND TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        tables = [row[0] for row in cursor.fetchall()]

        console.print(f"\n[bold]Schema: [{schema}][/bold]\n")
        console.print(f"{'Table':<40} {'Rows':>10} {'PK':>5} {'FKs':>5}")
        console.print("-" * 65)

        total_rows = 0
        for table in tables:
            # Row count
            cursor.execute(f"SELECT COUNT(*) FROM [{schema}].[{table}]")
            rows = cursor.fetchone()[0]
            total_rows += rows

            # Check for PK
            cursor.execute(f"""
                SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
                WHERE TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{table}'
                AND CONSTRAINT_TYPE = 'PRIMARY KEY'
            """)
            has_pk = "Yes" if cursor.fetchone()[0] > 0 else "No"

            # Count FKs
            cursor.execute(f"""
                SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
                WHERE TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{table}'
                AND CONSTRAINT_TYPE = 'FOREIGN KEY'
            """)
            fk_count = cursor.fetchone()[0]

            console.print(f"{table:<40} {rows:>10,} {has_pk:>5} {fk_count:>5}")

        console.print("-" * 65)
        console.print(f"{'TOTAL':<40} {total_rows:>10,}")
        console.print(f"\nTables: {len(tables)}")

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app()
