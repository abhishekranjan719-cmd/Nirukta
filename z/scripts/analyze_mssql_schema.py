#!/usr/bin/env python3
"""
MS SQL Schema Analyzer v2 with Enhanced NL2SQL Support

This script analyzes MS SQL database schemas and provides detailed metadata,
DDL, constraints, and LLM-powered recommendations specifically designed for
NL2SQL (Natural Language to SQL) engines.

New features in v2:
- DDL extraction for each table
- Enhanced constraint extraction with NL2SQL descriptions
- NL2SQL failure pattern analysis with proactive data quality detection
- Detailed table/column descriptions with analysis capabilities
- Business question mapping for each entity
- Schema-level analysis recommendations

FUNCTION CLASSIFICATION:

DATA-AGNOSTIC FUNCTIONS (work with any MS SQL schema without changes):
  - Database operations: connect(), get_tables(), get_table_ddl(), get_constraints_detailed(),
    get_table_metadata(), get_column_statistics()
    → Use standard SQL queries and INFORMATION_SCHEMA views

  - Data preparation: _prepare_schema_summary_basic(), _prepare_table_context(),
    _prepare_column_template(), _prepare_data_quality_findings_summary()
    → Format collected data without assumptions

  - LLM orchestration: _llm_call_with_retry(), analyze_with_llm(), analyze(),
    _analyze_schema_assessment(), _analyze_failure_patterns(), _analyze_recommendations(),
    _analyze_table_detailed()
    → Coordinate analysis using provided data

DATA-DEPENDENT FUNCTION (may need customization for different naming conventions):
  - _detect_data_quality_issues() - Contains hardcoded pattern matching:

    WHY IT'S DATA-DEPENDENT:
    • Line 590: if 'date' in col_name → Assumes English 'date' keyword
    • Line 602: ['amount','price','cost','total','quantity','qty'] → English numeric terms
    • Line 630: col_name.endswith('_id') → Assumes '_id' suffix for foreign keys
    • Line 668: ['total','sum','count','avg','average'] → English aggregation terms
    • Line 678: ['discount','adjustment','fee','tax'] → English business terms

    WHEN TO CUSTOMIZE:
    • Non-English schemas (e.g., German: 'datum' not 'date', 'preis' not 'price')
    • Different FK patterns (e.g., 'id_' prefix, 'fk_' prefix, no suffix)
    • Domain-specific terminology (medical: 'dx_', financial: 'amt_', etc.)
    • Alternative naming conventions (camelCase, different separators)

    HOW TO CUSTOMIZE:
    1. Locate _detect_data_quality_issues() method
    2. Update keyword lists for your naming convention
    3. Adjust pattern matching logic (e.g., startswith vs endswith)
    4. Add domain-specific patterns as needed

Requirements:
    pip install pyodbc sqlalchemy httpx python-dotenv

Usage:
    python analyze_mssql_schema.py --schema seed_data_raw --output analysis.json
"""

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
import pyodbc
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Fix Windows console encoding for Unicode output
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class LiteLLMClient:
    """Simple LiteLLM client for schema analysis"""

    def __init__(
        self,
        base_url: str = "http://localhost:4000",
        master_key: str = None,
        model: str = "gpt-4.1",
    ):
        self.base_url = base_url
        self.master_key = master_key or os.getenv("LITELLM_MASTER_KEY")
        self.model = model

        if not self.master_key:
            raise ValueError("LITELLM_MASTER_KEY must be set in environment or provided")

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=180.0,  # Increased timeout for detailed analysis
            verify=False,
            headers={
                "Authorization": f"Bearer {self.master_key}",
                "Content-Type": "application/json",
            },
        )

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.1,
        max_tokens: int = 32000,
    ) -> str:
        """Call LiteLLM chat completions API"""
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            response = await self.client.post(
                "/v1/chat/completions",
                json=payload,
            )
            response.raise_for_status()
            result = response.json()

            return result["choices"][0]["message"]["content"]

        except httpx.HTTPStatusError as e:
            raise Exception(f"LiteLLM HTTP error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            raise Exception(f"LiteLLM request error: {e!s}")

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


class MSSQLSchemaAnalyzerV2:
    """Enhanced analyzer for MS SQL database schemas with NL2SQL focus"""

    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        username: str,
        password: str,
        schema: str,
        litellm_client: LiteLLMClient,
        high_cardinality_threshold: int = 200,
    ):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.schema = schema
        self.litellm_client = litellm_client
        self.high_cardinality_threshold = high_cardinality_threshold

        # Build connection string
        # Note: Do NOT URL encode the password for pyodbc
        self.conn_str = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={host},{port};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            f"TrustServerCertificate=yes"
        )

        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            self.conn = pyodbc.connect(self.conn_str, timeout=10)
            self.cursor = self.conn.cursor()
            print(f"✅ Connected to {self.database} database")
        except Exception as e:
            raise Exception(f"Failed to connect to MS SQL: {e}")

    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def get_tables(self) -> list[str]:
        """Get all tables in the schema"""
        query = """
            SELECT TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = ? AND TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """
        self.cursor.execute(query, self.schema)
        return [row[0] for row in self.cursor.fetchall()]

    def get_table_ddl(self, table_name: str) -> str:
        """Generate DDL for a table"""
        print("  Extracting DDL...")

        ddl_parts = [f"CREATE TABLE [{self.schema}].[{table_name}] ("]

        # Get columns
        columns_query = """
            SELECT
                c.COLUMN_NAME,
                c.DATA_TYPE,
                c.CHARACTER_MAXIMUM_LENGTH,
                c.NUMERIC_PRECISION,
                c.NUMERIC_SCALE,
                c.IS_NULLABLE,
                c.COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS c
            WHERE c.TABLE_SCHEMA = ? AND c.TABLE_NAME = ?
            ORDER BY c.ORDINAL_POSITION
        """
        self.cursor.execute(columns_query, self.schema, table_name)

        column_defs = []
        for row in self.cursor.fetchall():
            col_name = row[0]
            data_type = row[1]
            max_length = row[2]
            precision = row[3]
            scale = row[4]
            is_nullable = row[5]
            default_value = row[6]

            # Build column definition
            if max_length and data_type in ["varchar", "nvarchar", "char", "nchar"]:
                type_str = f"{data_type}({max_length if max_length > 0 else 'max'})"
            elif precision and data_type in ["decimal", "numeric"]:
                type_str = f"{data_type}({precision},{scale or 0})"
            else:
                type_str = data_type

            nullable_str = "" if is_nullable == "YES" else " NOT NULL"
            default_str = f" DEFAULT {default_value}" if default_value else ""

            column_defs.append(f"    [{col_name}] {type_str}{nullable_str}{default_str}")

        ddl_parts.append(",\n".join(column_defs))
        ddl_parts.append(");")

        return "\n".join(ddl_parts)

    def get_constraints_detailed(self, table_name: str) -> dict[str, Any]:
        """Extract detailed constraint information with NL2SQL descriptions"""
        print("  Extracting constraints...")

        constraints = {
            "primary_key": None,
            "foreign_keys": [],
            "unique_constraints": [],
            "check_constraints": [],
            "nl2sql_descriptions": [],
        }

        # Get primary key with details
        pk_query = """
            SELECT
                tc.CONSTRAINT_NAME,
                STRING_AGG(c.COLUMN_NAME, ', ') WITHIN GROUP (ORDER BY c.COLUMN_NAME) AS pk_columns
            FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
            JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE c
                ON tc.CONSTRAINT_NAME = c.CONSTRAINT_NAME
                AND tc.TABLE_SCHEMA = c.TABLE_SCHEMA
                AND tc.TABLE_NAME = c.TABLE_NAME
            WHERE tc.TABLE_SCHEMA = ?
                AND tc.TABLE_NAME = ?
                AND tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
            GROUP BY tc.CONSTRAINT_NAME
        """
        self.cursor.execute(pk_query, self.schema, table_name)
        pk_row = self.cursor.fetchone()

        if pk_row:
            pk_columns = pk_row[1].split(", ")
            constraints["primary_key"] = {
                "constraint_name": pk_row[0],
                "columns": pk_columns,
                "ddl": f"ALTER TABLE [{self.schema}].[{table_name}] ADD CONSTRAINT [{pk_row[0]}] PRIMARY KEY ({', '.join([f'[{c}]' for c in pk_columns])})",
            }
            constraints["nl2sql_descriptions"].append(
                f"The table '{table_name}' is uniquely identified by {', '.join(pk_columns)}. "
                f"Use {'this column' if len(pk_columns) == 1 else 'these columns'} for exact record lookups."
            )

        # Get foreign keys with details
        fk_query = """
            SELECT
                fk.name AS constraint_name,
                col.name AS column_name,
                ref_schema.name AS referenced_schema,
                ref_table.name AS referenced_table,
                ref_col.name AS referenced_column
            FROM sys.foreign_keys fk
            INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
            INNER JOIN sys.tables t ON fk.parent_object_id = t.object_id
            INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
            INNER JOIN sys.columns col ON fkc.parent_object_id = col.object_id
                AND fkc.parent_column_id = col.column_id
            INNER JOIN sys.tables ref_table ON fkc.referenced_object_id = ref_table.object_id
            INNER JOIN sys.schemas ref_schema ON ref_table.schema_id = ref_schema.schema_id
            INNER JOIN sys.columns ref_col ON fkc.referenced_object_id = ref_col.object_id
                AND fkc.referenced_column_id = ref_col.column_id
            WHERE s.name = ? AND t.name = ?
        """
        self.cursor.execute(fk_query, self.schema, table_name)

        for row in self.cursor.fetchall():
            fk_info = {
                "constraint_name": row[0],
                "column": row[1],
                "references": {"schema": row[2], "table": row[3], "column": row[4]},
                "ddl": f"ALTER TABLE [{self.schema}].[{table_name}] ADD CONSTRAINT [{row[0]}] "
                f"FOREIGN KEY ([{row[1]}]) REFERENCES [{row[2]}].[{row[3]}] ([{row[4]}])",
            }
            constraints["foreign_keys"].append(fk_info)

            constraints["nl2sql_descriptions"].append(
                f"To join '{table_name}' with '{row[3]}', use: "
                f"{table_name}.{row[1]} = {row[3]}.{row[4]}. "
                f"This establishes the relationship between these tables."
            )

        return constraints

    def get_table_metadata(self, table_name: str) -> dict[str, Any]:
        """Extract comprehensive metadata for a table"""
        print(f"\n📊 Analyzing table: {self.schema}.{table_name}")

        metadata = {
            "table_name": table_name,
            "schema": self.schema,
            "columns": [],
            "primary_keys": [],
            "foreign_keys": [],
            "row_count": 0,
            "ddl": "",
            "constraints": {},
        }

        # Get row count
        count_query = f"SELECT COUNT(*) FROM [{self.schema}].[{table_name}]"
        self.cursor.execute(count_query)
        metadata["row_count"] = self.cursor.fetchone()[0]
        print(f"  Row count: {metadata['row_count']:,}")

        # Get column information
        columns_query = """
            SELECT
                c.COLUMN_NAME,
                c.DATA_TYPE,
                c.CHARACTER_MAXIMUM_LENGTH,
                c.NUMERIC_PRECISION,
                c.NUMERIC_SCALE,
                c.IS_NULLABLE,
                c.COLUMN_DEFAULT,
                c.ORDINAL_POSITION
            FROM INFORMATION_SCHEMA.COLUMNS c
            WHERE c.TABLE_SCHEMA = ? AND c.TABLE_NAME = ?
            ORDER BY c.ORDINAL_POSITION
        """
        self.cursor.execute(columns_query, self.schema, table_name)

        for row in self.cursor.fetchall():
            column_name = row[0]
            data_type = row[1]
            max_length = row[2]
            precision = row[3]
            scale = row[4]
            is_nullable = row[5] == "YES"
            default_value = row[6]
            ordinal = row[7]

            # Build data type string
            if max_length and data_type in ["varchar", "nvarchar", "char", "nchar"]:
                full_type = f"{data_type}({max_length if max_length > 0 else 'max'})"
            elif precision and data_type in ["decimal", "numeric"]:
                full_type = f"{data_type}({precision},{scale or 0})"
            else:
                full_type = data_type

            column_info = {
                "column_name": column_name,
                "data_type": data_type,
                "full_data_type": full_type,
                "max_length": max_length,
                "precision": precision,
                "scale": scale,
                "is_nullable": is_nullable,
                "default_value": default_value,
                "ordinal_position": ordinal,
            }

            # Get actual data statistics
            stats = self.get_column_statistics(table_name, column_name, data_type)
            column_info.update(stats)

            metadata["columns"].append(column_info)

        print(f"  Columns: {len(metadata['columns'])}")

        # Get primary keys (simple list)
        pk_query = """
            SELECT c.COLUMN_NAME
            FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
            JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE c
                ON tc.CONSTRAINT_NAME = c.CONSTRAINT_NAME
                AND tc.TABLE_SCHEMA = c.TABLE_SCHEMA
                AND tc.TABLE_NAME = c.TABLE_NAME
            WHERE tc.TABLE_SCHEMA = ?
                AND tc.TABLE_NAME = ?
                AND tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
            ORDER BY c.COLUMN_NAME
        """
        self.cursor.execute(pk_query, self.schema, table_name)
        metadata["primary_keys"] = [row[0] for row in self.cursor.fetchall()]

        # Get foreign keys (simple list)
        fk_query = """
            SELECT
                fk.name AS constraint_name,
                col.name AS column_name,
                ref_schema.name AS referenced_schema,
                ref_table.name AS referenced_table,
                ref_col.name AS referenced_column
            FROM sys.foreign_keys fk
            INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
            INNER JOIN sys.tables t ON fk.parent_object_id = t.object_id
            INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
            INNER JOIN sys.columns col ON fkc.parent_object_id = col.object_id
                AND fkc.parent_column_id = col.column_id
            INNER JOIN sys.tables ref_table ON fkc.referenced_object_id = ref_table.object_id
            INNER JOIN sys.schemas ref_schema ON ref_table.schema_id = ref_schema.schema_id
            INNER JOIN sys.columns ref_col ON fkc.referenced_object_id = ref_col.object_id
                AND fkc.referenced_column_id = ref_col.column_id
            WHERE s.name = ? AND t.name = ?
        """
        self.cursor.execute(fk_query, self.schema, table_name)

        for row in self.cursor.fetchall():
            metadata["foreign_keys"].append(
                {
                    "constraint_name": row[0],
                    "column_name": row[1],
                    "referenced_schema": row[2],
                    "referenced_table": row[3],
                    "referenced_column": row[4],
                }
            )

        # Extract DDL
        metadata["ddl"] = self.get_table_ddl(table_name)

        # Extract detailed constraints
        metadata["constraints"] = self.get_constraints_detailed(table_name)

        return metadata

    def get_column_statistics(self, table_name: str, column_name: str, data_type: str) -> dict[str, Any]:
        """Get detailed statistics for a column"""
        stats = {
            "distinct_count": 0,
            "null_count": 0,
            "null_percentage": 0.0,
            "is_high_cardinality": False,
            "sample_values": [],
            "actual_max_length": None,
            "suggested_buffer_length": None,
        }

        try:
            # Get distinct and null counts
            count_query = f"""
                SELECT
                    COUNT(DISTINCT [{column_name}]) AS distinct_count,
                    SUM(CASE WHEN [{column_name}] IS NULL THEN 1 ELSE 0 END) AS null_count,
                    COUNT(*) AS total_count
                FROM [{self.schema}].[{table_name}]
            """
            self.cursor.execute(count_query)
            row = self.cursor.fetchone()

            distinct_count = row[0] or 0
            null_count = row[1] or 0
            total_count = row[2] or 0

            stats["distinct_count"] = distinct_count
            stats["null_count"] = null_count
            stats["null_percentage"] = round((null_count / total_count * 100), 2) if total_count > 0 else 0

            # Check high cardinality for categorical columns
            if data_type in ["varchar", "nvarchar", "char", "nchar", "int", "bigint", "smallint"]:
                stats["is_high_cardinality"] = distinct_count > self.high_cardinality_threshold

            # Get actual max length for string columns
            if data_type in ["varchar", "nvarchar", "char", "nchar"]:
                length_query = f"""
                    SELECT MAX(LEN([{column_name}])) AS max_length
                    FROM [{self.schema}].[{table_name}]
                    WHERE [{column_name}] IS NOT NULL
                """
                self.cursor.execute(length_query)
                max_len_row = self.cursor.fetchone()
                if max_len_row and max_len_row[0]:
                    actual_max = max_len_row[0]
                    stats["actual_max_length"] = actual_max
                    # Suggest buffer: 1.5x actual max, rounded up to nearest 10
                    stats["suggested_buffer_length"] = ((int(actual_max * 1.5) + 9) // 10) * 10

            # Get top 10 sample values by frequency
            if distinct_count > 0 and distinct_count <= 10000:  # Only for reasonable cardinality
                sample_query = f"""
                    SELECT TOP 10
                        [{column_name}] AS value,
                        COUNT(*) AS frequency,
                        CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS DECIMAL(5,2)) AS percentage
                    FROM [{self.schema}].[{table_name}]
                    WHERE [{column_name}] IS NOT NULL
                    GROUP BY [{column_name}]
                    ORDER BY COUNT(*) DESC
                """
                self.cursor.execute(sample_query)

                for sample_row in self.cursor.fetchall():
                    value = sample_row[0]
                    # Convert to string, handle different types
                    if isinstance(value, (bytes, bytearray)):
                        value_str = value.decode("utf-8", errors="replace")
                    else:
                        value_str = str(value)

                    stats["sample_values"].append(
                        {
                            "value": value_str,
                            "frequency": sample_row[1],
                            "percentage": float(sample_row[2]),
                        }
                    )

        except Exception as e:
            print(f"    ⚠️  Failed to get statistics for {column_name}: {e}")

        return stats

    def _detect_data_quality_issues(self, schema_metadata: dict[str, Any]) -> dict[str, Any]:
        """Detect concrete data quality issues that could cause NL2SQL failures"""
        print("  🔍 Detecting data quality issues...")

        issues = {
            "wrong_table_selection_risks": [],
            "wrong_column_selection_risks": [],
            "wrong_filter_condition_risks": [],
            "wrong_join_condition_risks": [],
            "wrong_aggregation_risks": [],
        }

        # Build column name index across all tables
        column_index = {}
        for table in schema_metadata["tables"]:
            for col in table["columns"]:
                col_name = col["column_name"].lower()
                if col_name not in column_index:
                    column_index[col_name] = []
                column_index[col_name].append(
                    {"table": table["table_name"], "full_type": col["full_data_type"], "nullable": col["is_nullable"]}
                )

        # 1. Detect wrong table selection risks
        table_names = [t["table_name"] for t in schema_metadata["tables"]]
        for i, t1 in enumerate(table_names):
            for t2 in table_names[i + 1 :]:
                # Check for similar names
                if t1.lower() in t2.lower() or t2.lower() in t1.lower():
                    issues["wrong_table_selection_risks"].append(
                        {
                            "tables": [t1, t2],
                            "issue": f"Similar table names '{t1}' and '{t2}' may confuse NL2SQL",
                            "example": f"User asks about items but system might query '{t1}' instead of '{t2}'",
                        }
                    )

        # Check for tables without primary keys
        for table in schema_metadata["tables"]:
            if not table["primary_keys"]:
                issues["wrong_table_selection_risks"].append(
                    {
                        "table": table["table_name"],
                        "issue": "Missing primary key makes table harder to identify uniquely",
                        "recommendation": f"Add PRIMARY KEY constraint to {table['table_name']}",
                    }
                )

        # 2. Detect wrong column selection risks (duplicate column names)
        for col_name, occurrences in column_index.items():
            if len(occurrences) > 1:
                # Same column name in multiple tables
                tables = [occ["table"] for occ in occurrences]
                types = [occ["full_type"] for occ in occurrences]

                issues["wrong_column_selection_risks"].append(
                    {
                        "column": col_name,
                        "tables": tables,
                        "data_types": types,
                        "issue": f"Column '{col_name}' exists in {len(occurrences)} tables: {', '.join(tables)}",
                        "risk": "NL2SQL may select wrong table when filtering/grouping by this column",
                    }
                )

        # 3. Detect wrong filter condition risks
        for table in schema_metadata["tables"]:
            for col in table["columns"]:
                col_name = col["column_name"]
                data_type = col["data_type"].lower()

                # Date stored as varchar
                if "date" in col_name.lower() and data_type in ["varchar", "nvarchar", "char", "nchar", "text"]:
                    issues["wrong_filter_condition_risks"].append(
                        {
                            "table": table["table_name"],
                            "column": col_name,
                            "data_type": col["full_data_type"],
                            "issue": "Date column stored as text/varchar",
                            "wrong_example": f"WHERE {col_name} > '2024-01-01'",
                            "correct_example": f"WHERE CAST({col_name} AS DATE) > '2024-01-01'",
                            "recommendation": f"Convert {table['table_name']}.{col_name} to DATE or DATETIME type",
                        }
                    )

                # Numeric stored as varchar
                if any(
                    kw in col_name.lower() for kw in ["amount", "price", "cost", "total", "quantity", "qty"]
                ) and data_type in ["varchar", "nvarchar", "char", "nchar", "text"]:
                    issues["wrong_filter_condition_risks"].append(
                        {
                            "table": table["table_name"],
                            "column": col_name,
                            "data_type": col["full_data_type"],
                            "issue": "Numeric column stored as text/varchar",
                            "wrong_example": f"WHERE {col_name} > 100",
                            "correct_example": f"WHERE CAST({col_name} AS DECIMAL) > 100",
                            "recommendation": f"Convert {table['table_name']}.{col_name} to appropriate numeric type",
                        }
                    )

                # High null percentage
                if col.get("null_percentage", 0) > 50:
                    issues["wrong_filter_condition_risks"].append(
                        {
                            "table": table["table_name"],
                            "column": col_name,
                            "null_percentage": col.get("null_percentage", 0),
                            "issue": f"High NULL percentage ({col.get('null_percentage', 0):.1f}%)",
                            "risk": "Filtering may miss many records; aggregations may be misleading",
                            "recommendation": f"Handle NULLs explicitly: WHERE {col_name} IS NOT NULL",
                        }
                    )

        # 4. Detect wrong join condition risks
        for table in schema_metadata["tables"]:
            # Check for FK columns without constraints
            for col in table["columns"]:
                col_name = col["column_name"].lower()
                # Potential FK pattern: ends with _id or matches another table name
                if col_name.endswith("_id") or any(
                    t["table_name"].lower() in col_name for t in schema_metadata["tables"]
                ):
                    # Check if there's a FK constraint
                    has_fk = any(
                        fk["column_name"].lower() == col["column_name"].lower() for fk in table["foreign_keys"]
                    )

                    if not has_fk and col["column_name"].lower() not in [pk.lower() for pk in table["primary_keys"]]:
                        # Try to find potential reference table
                        potential_ref = col_name.replace("_id", "")
                        matching_tables = [
                            t["table_name"]
                            for t in schema_metadata["tables"]
                            if potential_ref in t["table_name"].lower()
                        ]

                        if matching_tables:
                            issues["wrong_join_condition_risks"].append(
                                {
                                    "table": table["table_name"],
                                    "column": col["column_name"],
                                    "issue": "Potential FK column without constraint",
                                    "potential_references": matching_tables,
                                    "risk": "NL2SQL may not detect relationship, causing incorrect joins",
                                    "recommendation": "Add FK constraint or clarify relationship in documentation",
                                }
                            )

            # Check for missing indexes on FK columns
            for fk in table["foreign_keys"]:
                issues["wrong_join_condition_risks"].append(
                    {
                        "table": table["table_name"],
                        "column": fk["column_name"],
                        "references": f"{fk['referenced_table']}.{fk['referenced_column']}",
                        "issue": "FK relationship exists but may lack index",
                        "recommendation": f"Ensure index exists on {table['table_name']}.{fk['column_name']} for join performance",
                    }
                )

        # 5. Detect wrong aggregation risks
        for table in schema_metadata["tables"]:
            for col in table["columns"]:
                col_name = col["column_name"].lower()

                # Detect potential aggregation columns
                if any(kw in col_name for kw in ["total", "sum", "count", "avg", "average"]):
                    issues["wrong_aggregation_risks"].append(
                        {
                            "table": table["table_name"],
                            "column": col["column_name"],
                            "issue": "Pre-aggregated column name suggests already computed value",
                            "risk": "Aggregating this column again (SUM/AVG) may cause double-counting",
                            "recommendation": f"Use {col['column_name']} directly, avoid SUM({col['column_name']})",
                        }
                    )

                # Detect discount/adjustment columns that exist at multiple levels
                if any(kw in col_name for kw in ["discount", "adjustment", "fee", "tax"]):
                    # Check if similar column exists in related tables
                    related_tables = set()
                    for fk in table["foreign_keys"]:
                        related_tables.add(fk["referenced_table"])

                    for rel_table_name in related_tables:
                        rel_table = next(
                            (t for t in schema_metadata["tables"] if t["table_name"] == rel_table_name), None
                        )
                        if rel_table:
                            for rel_col in rel_table["columns"]:
                                if any(
                                    kw in rel_col["column_name"].lower()
                                    for kw in ["discount", "adjustment", "fee", "tax"]
                                ):
                                    issues["wrong_aggregation_risks"].append(
                                        {
                                            "tables": [table["table_name"], rel_table_name],
                                            "columns": [col["column_name"], rel_col["column_name"]],
                                            "issue": "Similar columns in related tables may cause confusion",
                                            "risk": "NL2SQL may aggregate at wrong level or double-count",
                                            "recommendation": f"Clarify whether to sum at {table['table_name']} or {rel_table_name} level",
                                        }
                                    )
                                    break

        print(f"    Found {len(issues['wrong_table_selection_risks'])} table selection risks")
        print(f"    Found {len(issues['wrong_column_selection_risks'])} column selection risks")
        print(f"    Found {len(issues['wrong_filter_condition_risks'])} filter condition risks")
        print(f"    Found {len(issues['wrong_join_condition_risks'])} join condition risks")
        print(f"    Found {len(issues['wrong_aggregation_risks'])} aggregation risks")

        return issues

    async def _llm_call_with_retry(
        self, messages: list[dict[str, str]], max_tokens: int = 8000, call_name: str = "LLM call",
        max_retries: int = 5, validate_json: bool = True
    ) -> str:
        """Make an LLM call with retry logic, rate limit handling, and JSON validation

        Args:
            messages: Chat messages to send
            max_tokens: Maximum tokens for response
            call_name: Name for logging purposes
            max_retries: Maximum number of retry attempts
            validate_json: Whether to validate response as JSON and retry if invalid

        Returns:
            Cleaned response string (JSON if validate_json=True)
        """
        import asyncio as aio

        last_error = None
        last_response = None

        for attempt in range(max_retries):
            try:
                response = await self.litellm_client.chat_completion(
                    messages=messages,
                    temperature=0.1,
                    max_tokens=max_tokens,
                )

                # Check for empty response
                if not response or not response.strip():
                    print(f"⚠️  {call_name} - Empty response on attempt {attempt + 1}/{max_retries}")
                    if attempt < max_retries - 1:
                        wait_time = 5 * (attempt + 1)  # 5, 10, 15, 20, 25 seconds
                        print(f"    Retrying in {wait_time}s...")
                        await aio.sleep(wait_time)
                        continue
                    else:
                        raise Exception("LLM returned empty response")

                # Clean up response - remove markdown code blocks
                response = response.strip()
                if response.startswith("```json"):
                    response = response[7:]
                if response.startswith("```"):
                    response = response[3:]
                if response.endswith("```"):
                    response = response[:-3]
                response = response.strip()
                last_response = response

                # Validate JSON if required
                if validate_json:
                    try:
                        json.loads(response)
                    except json.JSONDecodeError as je:
                        print(f"⚠️  {call_name} - Invalid JSON on attempt {attempt + 1}/{max_retries}: {je}")
                        if attempt < max_retries - 1:
                            wait_time = 5 * (attempt + 1)  # 5, 10, 15, 20, 25 seconds
                            print(f"    Retrying in {wait_time}s...")
                            await aio.sleep(wait_time)
                            continue
                        else:
                            # On final attempt, try to salvage partial JSON
                            raise

                return response

            except Exception as e:
                last_error = e
                error_str = str(e).lower()

                # Check for rate limit error
                is_rate_limit = any(term in error_str for term in ['rate limit', 'rate_limit', '429', 'too many requests', 'quota'])

                if is_rate_limit:
                    print(f"⚠️  {call_name} - Rate limit hit on attempt {attempt + 1}/{max_retries}")
                    if attempt < max_retries - 1:
                        print(f"    Sleeping for 60 seconds before retry...")
                        await aio.sleep(60)  # Sleep 1 minute for rate limit
                        continue
                else:
                    print(f"⚠️  {call_name} - Error on attempt {attempt + 1}/{max_retries}: {e}")
                    if attempt < max_retries - 1:
                        wait_time = 5 * (attempt + 1)  # 5, 10, 15, 20, 25 seconds
                        print(f"    Retrying in {wait_time}s...")
                        await aio.sleep(wait_time)
                        continue

                # If we've exhausted retries, raise the error
                if attempt == max_retries - 1:
                    raise

        # Should not reach here, but just in case
        if last_error:
            raise last_error
        raise Exception(f"{call_name} failed after {max_retries} attempts")

    async def _analyze_schema_assessment(self, schema_metadata: dict[str, Any]) -> dict[str, Any]:
        """LLM Call 1: Schema-level assessment and high-level description"""
        print("  🔍 Call 1/4+: Schema assessment & description...")

        schema_summary = self._prepare_schema_summary_basic(schema_metadata)

        prompt = f"""You are a database schema expert specializing in SQL Server and NL2SQL systems.

Analyze this database schema and provide a high-level assessment.

SCHEMA SUMMARY:
{schema_summary}

Provide analysis in JSON format:

{{
  "schema_assessment": {{
    "overall_quality": "excellent|good|fair|needs_improvement",
    "normalization_level": "1NF|2NF|3NF|BCNF|denormalized|mixed",
    "suitability_for_nl2sql": "excellent|good|fair|poor",
    "complexity": "simple|moderate|complex",
    "summary": "2-3 sentence overall assessment of the schema quality and structure"
  }},

  "schema_description": "Comprehensive description (3-5 sentences) including: (1) domain/industry, (2) key entities and their purposes, (3) overall data model structure, (4) what business analyses are possible, (5) top 5 business questions that can be answered with this schema",

  "table_relationships_overview": {{
    "central_tables": ["List of core/fact tables"],
    "lookup_tables": ["List of dimension/reference tables"],
    "relationship_summary": "How tables connect and what analytical paths are possible"
  }}
}}

Return ONLY valid JSON."""

        messages = [
            {"role": "system", "content": "You are a database schema expert. Respond only with valid JSON."},
            {"role": "user", "content": prompt},
        ]

        response = None
        try:
            response = await self._llm_call_with_retry(messages, max_tokens=3000, call_name="Schema assessment")
            return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"⚠️  JSON parse error: {e}")
            return {"error": "JSON parse failed", "raw_response": response or "No response received"}
        except Exception as e:
            return {"error": str(e), "raw_response": response or "No response received"}

    async def _analyze_failure_patterns(
        self, schema_metadata: dict[str, Any], data_quality_issues: dict[str, Any]
    ) -> dict[str, Any]:
        """LLM Call 2: NL2SQL failure pattern analysis with concrete data quality findings"""
        print("  🔍 Call 2/4+: NL2SQL failure patterns...")

        schema_summary = self._prepare_schema_summary_basic(schema_metadata)

        # Prepare concrete findings summary
        findings_summary = self._prepare_data_quality_findings_summary(data_quality_issues)

        prompt = f"""You are an NL2SQL expert. Analyze this schema for common failure patterns.

SCHEMA SUMMARY:
{schema_summary}

CONCRETE DATA QUALITY ISSUES DETECTED:
{findings_summary}

Based on the CONCRETE ISSUES above, provide specific failure pattern analysis in JSON format:

{{
  "nl2sql_failure_patterns": {{
    "wrong_table_selection": [
      {{
        "scenario": "Description of user intent",
        "issue": "Why NL2SQL might select wrong table (use concrete examples from ISSUES)",
        "example": "User asks: 'X' but system queries table Y instead of Z",
        "mitigation": "How to prevent this (specific to detected issues)"
      }}
    ],
    "wrong_column_selection": [
      {{
        "table": "table_name",
        "column": "column_name",
        "issue": "Why this column might be confused (reference detected duplicate columns)",
        "similar_columns": ["list of actual columns from ISSUES"],
        "mitigation": "How to disambiguate in NL2SQL"
      }}
    ],
    "wrong_filter_conditions": [
      {{
        "table": "table_name",
        "column": "column_name",
        "issue": "Common filtering mistakes (use detected date/numeric type issues)",
        "wrong_example": "Incorrect SQL approach",
        "correct_example": "Correct SQL approach with CAST if needed",
        "data_type_consideration": "Reference actual data types from ISSUES"
      }}
    ],
    "wrong_join_conditions": [
      {{
        "tables": ["table1", "table2"],
        "issue": "Why join might fail (reference missing FK constraints from ISSUES)",
        "correct_join": "Proper JOIN syntax with ON clause",
        "common_mistake": "What NL2SQL systems typically do wrong",
        "mitigation": "How to handle this correctly"
      }}
    ],
    "wrong_aggregation": [
      {{
        "table": "table_name",
        "column": "column_name",
        "issue": "Why aggregation might be incorrect (reference pre-aggregated columns from ISSUES)",
        "correct_usage": "Proper aggregation approach with example",
        "considerations": "NULL handling, data types, GROUP BY requirements, double-counting risks"
      }}
    ]
  }}
}}

IMPORTANT: Use the CONCRETE ISSUES detected above to provide specific, actionable examples.
Reference actual table names, column names, and data types from the schema.

Return ONLY valid JSON."""

        messages = [
            {"role": "system", "content": "You are an NL2SQL expert. Respond only with valid JSON."},
            {"role": "user", "content": prompt},
        ]

        response = None
        try:
            response = await self._llm_call_with_retry(messages, max_tokens=5000, call_name="Failure patterns")
            analysis = json.loads(response)

            # Add detected issues to the output
            if "nl2sql_failure_patterns" in analysis:
                analysis["nl2sql_failure_patterns"]["detected_data_quality_issues"] = data_quality_issues

            return analysis
        except json.JSONDecodeError as e:
            print(f"⚠️  JSON parse error: {e}")
            return {
                "error": "JSON parse failed",
                "raw_response": response or "No response received",
                "detected_data_quality_issues": data_quality_issues,
            }
        except Exception as e:
            return {"error": str(e), "raw_response": response or "No response received", "detected_data_quality_issues": data_quality_issues}

    def _prepare_data_quality_findings_summary(self, issues: dict[str, Any]) -> str:
        """Prepare a concise summary of detected data quality issues"""
        lines = []

        if issues["wrong_table_selection_risks"]:
            lines.append(f"\n1. WRONG TABLE SELECTION RISKS ({len(issues['wrong_table_selection_risks'])} issues):")
            for i, risk in enumerate(issues["wrong_table_selection_risks"][:5], 1):
                if "tables" in risk:
                    lines.append(f"   {i}. Similar tables: {', '.join(risk['tables'])}")
                elif "table" in risk:
                    lines.append(f"   {i}. {risk['table']}: {risk['issue']}")

        if issues["wrong_column_selection_risks"]:
            lines.append(f"\n2. WRONG COLUMN SELECTION RISKS ({len(issues['wrong_column_selection_risks'])} issues):")
            for i, risk in enumerate(issues["wrong_column_selection_risks"][:5], 1):
                lines.append(f"   {i}. Column '{risk['column']}' in tables: {', '.join(risk['tables'])}")

        if issues["wrong_filter_condition_risks"]:
            lines.append(f"\n3. WRONG FILTER CONDITION RISKS ({len(issues['wrong_filter_condition_risks'])} issues):")
            for i, risk in enumerate(issues["wrong_filter_condition_risks"][:5], 1):
                lines.append(f"   {i}. {risk.get('table', 'N/A')}.{risk.get('column', 'N/A')}: {risk['issue']}")

        if issues["wrong_join_condition_risks"]:
            lines.append(f"\n4. WRONG JOIN CONDITION RISKS ({len(issues['wrong_join_condition_risks'])} issues):")
            for i, risk in enumerate(issues["wrong_join_condition_risks"][:5], 1):
                if "potential_references" in risk:
                    lines.append(
                        f"   {i}. {risk['table']}.{risk['column']} -> potential FK to {risk['potential_references']}"
                    )
                else:
                    lines.append(f"   {i}. {risk['table']}.{risk['column']} -> {risk.get('references', 'N/A')}")

        if issues["wrong_aggregation_risks"]:
            lines.append(f"\n5. WRONG AGGREGATION RISKS ({len(issues['wrong_aggregation_risks'])} issues):")
            for i, risk in enumerate(issues["wrong_aggregation_risks"][:5], 1):
                if "columns" in risk:
                    lines.append(f"   {i}. Multi-level: {risk['tables']} have {risk['columns']}")
                else:
                    lines.append(f"   {i}. {risk.get('table', 'N/A')}.{risk.get('column', 'N/A')}: {risk['issue']}")

        return "\n".join(lines) if lines else "No critical data quality issues detected."

    async def _analyze_recommendations(
        self, schema_metadata: dict[str, Any], data_quality_issues: dict[str, Any]
    ) -> dict[str, Any]:
        """LLM Call 3: General recommendations for improvement with concrete findings"""
        print("  🔍 Call 3/4+: General recommendations...")

        schema_summary = self._prepare_schema_summary_basic(schema_metadata)
        findings_summary = self._prepare_data_quality_findings_summary(data_quality_issues)

        prompt = f"""You are a database design expert. Provide recommendations for this schema.

SCHEMA SUMMARY:
{schema_summary}

CONCRETE DATA QUALITY ISSUES DETECTED:
{findings_summary}

Based on the CONCRETE ISSUES above, analyze and provide specific, actionable recommendations in JSON format:

{{
  "recommendations": {{
    "data_types": [
      {{
        "table": "table_name",
        "column": "column_name",
        "current_type": "current data type from ISSUES",
        "suggested_type": "recommended data type",
        "reason": "Why this change would be beneficial (reference detected issues)"
      }}
    ],
    "naming_conventions": [
      {{
        "category": "tables|columns|constraints",
        "issue": "Current naming issue from schema",
        "suggestion": "How to improve naming",
        "examples": "Specific examples from detected issues"
      }}
    ],
    "normalization": [
      {{
        "table": "table_name",
        "issue": "Normalization issue description",
        "recommendation": "How to normalize properly",
        "benefit": "What this improves for NL2SQL"
      }}
    ],
    "constraints": [
      {{
        "table": "table_name",
        "constraint_type": "PRIMARY KEY|FOREIGN KEY|UNIQUE|CHECK|NOT NULL",
        "recommendation": "What constraint to add/modify (reference missing PKs/FKs from ISSUES)",
        "benefit": "Why this is important for data integrity and NL2SQL"
      }}
    ],
    "indexes": [
      {{
        "table": "table_name",
        "columns": ["column1", "column2"],
        "index_type": "CLUSTERED|NONCLUSTERED",
        "reason": "Why this index would improve performance (reference FK columns from ISSUES)"
      }}
    ]
  }}
}}

IMPORTANT: Prioritize recommendations based on CONCRETE ISSUES detected.
Focus on issues that impact NL2SQL query generation and execution.
Reference actual table names, column names, and data types from the detected issues.

Return ONLY valid JSON."""

        messages = [
            {"role": "system", "content": "You are a database design expert. Respond only with valid JSON."},
            {"role": "user", "content": prompt},
        ]

        response = None
        try:
            response = await self._llm_call_with_retry(messages, max_tokens=4000, call_name="Recommendations")
            analysis = json.loads(response)

            # Add detected issues summary to recommendations
            if "recommendations" in analysis:
                analysis["recommendations"]["based_on_detected_issues"] = {
                    "table_selection_risks_count": len(data_quality_issues["wrong_table_selection_risks"]),
                    "column_selection_risks_count": len(data_quality_issues["wrong_column_selection_risks"]),
                    "filter_condition_risks_count": len(data_quality_issues["wrong_filter_condition_risks"]),
                    "join_condition_risks_count": len(data_quality_issues["wrong_join_condition_risks"]),
                    "aggregation_risks_count": len(data_quality_issues["wrong_aggregation_risks"]),
                }

            return analysis
        except json.JSONDecodeError as e:
            print(f"⚠️  JSON parse error: {e}")
            return {"error": "JSON parse failed", "raw_response": response or "No response received"}
        except Exception as e:
            return {"error": str(e), "raw_response": response or "No response received"}

    async def _analyze_table_detailed(
        self, table_metadata: dict[str, Any], all_tables_context: list[str]
    ) -> dict[str, Any]:
        """LLM Call N: Detailed analysis for a single table"""
        table_name = table_metadata["table_name"]

        # Prepare detailed table context
        table_context = self._prepare_table_context(table_metadata, all_tables_context)

        prompt = f"""You are a database expert specializing in NL2SQL systems.

Analyze this table in detail for NL2SQL optimization.

TABLE CONTEXT:
{table_context}

Provide comprehensive analysis in JSON format:

{{
  "table_description": {{
    "purpose": "What this table represents and its role in the schema",
    "columns_present": {json.dumps([col['column_name'] for col in table_metadata['columns']])},
    "key_characteristics": "Important characteristics (cardinality, data patterns, etc.)",
    "analysis_capabilities": "What analyses can be performed with this table alone",
    "business_questions": [
      "Specific business question 1 this table can answer",
      "Specific business question 2 this table can answer",
      "Specific business question 3 this table can answer",
      "Specific business question 4 this table can answer",
      "Specific business question 5 this table can answer"
    ],
    "relationships": "How this table connects to others and what those relationships enable"
  }},

  "column_descriptions": {{
{self._prepare_column_template(table_metadata)}
  }}
}}

For EACH column, provide:
- description: What the column represents
- analysis_use: How it's used in analysis (filtering/grouping/aggregation/joins)
- business_questions: 2-3 specific questions this column helps answer
- nl2sql_hints: Critical considerations for NL2SQL (data types, common patterns, join keys)

Return ONLY valid JSON."""

        messages = [
            {
                "role": "system",
                "content": "You are a database expert specializing in NL2SQL. Respond only with valid JSON.",
            },
            {"role": "user", "content": prompt},
        ]

        response = None
        try:
            response = await self._llm_call_with_retry(
                messages, max_tokens=8000, call_name=f"Table analysis: {table_name}"
            )
            return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"⚠️  JSON parse error for table {table_name}: {e}")
            return {"error": "JSON parse failed", "raw_response": response or "No response received"}
        except Exception as e:
            return {"error": str(e), "raw_response": response or "No response received"}

    async def analyze_with_llm(self, schema_metadata: dict[str, Any]) -> dict[str, Any]:
        """Use LLM to analyze schema with multiple focused calls (max 10k tokens each)"""
        print("\n🤖 Analyzing schema with GPT-4.1 (Multi-call NL2SQL Analysis)...", flush=True)

        # First: Detect concrete data quality issues
        data_quality_issues = self._detect_data_quality_issues(schema_metadata)

        # Call 1: Schema assessment
        schema_assessment = await self._analyze_schema_assessment(schema_metadata)

        # Call 2: Failure patterns (with concrete data quality findings)
        failure_patterns = await self._analyze_failure_patterns(schema_metadata, data_quality_issues)

        # Call 3: Recommendations (with concrete data quality findings)
        recommendations = await self._analyze_recommendations(schema_metadata, data_quality_issues)

        # Calls 4-N: Per-table analysis
        print(f"  🔍 Analyzing {len(schema_metadata['tables'])} tables in detail...", flush=True)
        all_table_names = [t["table_name"] for t in schema_metadata["tables"]]

        table_descriptions = {}
        column_descriptions = {}

        for i, table_meta in enumerate(schema_metadata["tables"], 1):
            table_name = table_meta["table_name"]
            print(f"    📋 Table {i}/{len(schema_metadata['tables'])}: {table_name}", flush=True)

            table_analysis = await self._analyze_table_detailed(table_meta, all_table_names)

            if "error" not in table_analysis:
                if "table_description" in table_analysis:
                    table_descriptions[table_name] = table_analysis["table_description"]
                if "column_descriptions" in table_analysis:
                    column_descriptions[table_name] = table_analysis["column_descriptions"]
            else:
                print(f"      ⚠️  Table analysis had errors: {table_analysis.get('error', 'Unknown')}")
                table_descriptions[table_name] = {"error": table_analysis.get("error", "Analysis failed")}
                column_descriptions[table_name] = {"error": table_analysis.get("error", "Analysis failed")}

        # Combine all results
        combined_analysis = {
            **schema_assessment,
            **failure_patterns,
            **recommendations,
            "table_descriptions": table_descriptions,
            "column_descriptions": column_descriptions,
        }

        print("✅ LLM analysis completed (multiple focused calls)")
        return combined_analysis

    def _prepare_schema_summary_basic(self, schema_metadata: dict[str, Any]) -> str:
        """Prepare a basic schema summary for schema-level LLM calls"""
        summary_lines = [
            f"Schema: {self.schema}",
            f"Database: {self.database}",
            f"Tables: {len(schema_metadata['tables'])}",
            f"Total rows: {sum(t['row_count'] for t in schema_metadata['tables']):,}",
            "\nTable Overview:",
        ]

        for table in schema_metadata["tables"]:
            summary_lines.append(
                f"\n  {table['table_name']}: {table['row_count']:,} rows, " f"{len(table['columns'])} columns"
            )
            summary_lines.append(f"    PK: {', '.join(table['primary_keys']) or 'NONE'}")

            if table["foreign_keys"]:
                fk_summary = []
                for fk in table["foreign_keys"][:3]:  # Limit to first 3
                    fk_summary.append(f"{fk['column_name']}->{fk['referenced_table']}.{fk['referenced_column']}")
                if len(table["foreign_keys"]) > 3:
                    fk_summary.append(f"...+{len(table['foreign_keys']) - 3} more")
                summary_lines.append(f"    FK: {', '.join(fk_summary)}")

            # Add column names only
            col_names = [col["column_name"] for col in table["columns"]]
            summary_lines.append(f"    Columns: {', '.join(col_names)}")

        return "\n".join(summary_lines)

    def _prepare_table_context(self, table_metadata: dict[str, Any], all_tables: list[str]) -> str:
        """Prepare detailed context for a single table analysis"""
        table_name = table_metadata["table_name"]
        context_lines = [
            f"Table: {self.schema}.{table_name}",
            f"Row count: {table_metadata['row_count']:,}",
            f"Columns: {len(table_metadata['columns'])}",
            f"\nPrimary Keys: {', '.join(table_metadata['primary_keys']) or 'NONE'}",
        ]

        # Foreign keys
        if table_metadata["foreign_keys"]:
            context_lines.append("\nForeign Keys:")
            for fk in table_metadata["foreign_keys"]:
                context_lines.append(
                    f"  - {fk['column_name']} -> "
                    f"{fk['referenced_schema']}.{fk['referenced_table']}.{fk['referenced_column']}"
                )
        else:
            context_lines.append("\nForeign Keys: None")

        # Related tables (from FK relationships)
        related_tables = set()
        for fk in table_metadata["foreign_keys"]:
            related_tables.add(fk["referenced_table"])
        if related_tables:
            context_lines.append(f"\nRelated Tables: {', '.join(sorted(related_tables))}")

        # All available tables for context
        other_tables = [t for t in all_tables if t != table_name]
        if other_tables:
            context_lines.append(f"Other Tables in Schema: {', '.join(other_tables)}")

        # Detailed column information
        context_lines.append("\nColumn Details:")
        for col in table_metadata["columns"]:
            nullable = "NULL" if col["is_nullable"] else "NOT NULL"
            high_card = " [HIGH CARDINALITY]" if col.get("is_high_cardinality") else ""

            col_line = f"  - {col['column_name']}: {col['full_data_type']} {nullable}"

            if col.get("actual_max_length"):
                col_line += f" (max len: {col['actual_max_length']})"

            col_line += f" | distinct: {col.get('distinct_count', 0)}"

            if col.get("null_count", 0) > 0:
                col_line += f" | nulls: {col.get('null_percentage', 0):.1f}%"

            col_line += high_card
            context_lines.append(col_line)

            # Add sample values for low cardinality columns
            if col.get("sample_values") and len(col["sample_values"]) <= 10:
                samples = []
                for s in col["sample_values"][:5]:
                    val = s["value"][:40]  # Truncate long values
                    samples.append(f"{val} ({s['percentage']:.1f}%)")
                context_lines.append(f"    Top values: {', '.join(samples)}")

        # DDL
        if table_metadata.get("ddl"):
            context_lines.append(f"\nDDL:\n{table_metadata['ddl']}")

        return "\n".join(context_lines)

    def _prepare_column_template(self, table_metadata: dict[str, Any]) -> str:
        """Prepare JSON template structure for column descriptions"""
        template_lines = []
        for col in table_metadata["columns"]:
            col_name = col["column_name"]
            template_lines.append(f"""    "{col_name}": {{
      "description": "...",
      "analysis_use": "...",
      "business_questions": ["...", "..."],
      "nl2sql_hints": "..."
    }}""")

        return ",\n".join(template_lines)

    def _prepare_schema_summary(self, schema_metadata: dict[str, Any]) -> str:
        """Prepare a detailed schema summary for LLM (legacy method, kept for compatibility)"""
        summary_lines = [
            f"Schema: {self.schema}",
            f"Tables: {len(schema_metadata['tables'])}",
            f"Total rows: {sum(t['row_count'] for t in schema_metadata['tables']):,}",
            "\nDetailed Table Information:",
        ]

        for table in schema_metadata["tables"]:
            summary_lines.append(f"\n  TABLE: {table['table_name']} ({table['row_count']:,} rows)")
            summary_lines.append(f"    Primary Keys: {', '.join(table['primary_keys']) or 'MISSING - NO PRIMARY KEY'}")

            if table["foreign_keys"]:
                summary_lines.append("    Foreign Keys:")
                for fk in table["foreign_keys"]:
                    summary_lines.append(
                        f"      - {fk['column_name']} -> "
                        f"{fk['referenced_schema']}.{fk['referenced_table']}.{fk['referenced_column']}"
                    )
            else:
                summary_lines.append("    Foreign Keys: None")

            summary_lines.append(f"    Columns ({len(table['columns'])}):")
            for col in table["columns"]:
                nullable = "NULL" if col["is_nullable"] else "NOT NULL"
                high_card = " [HIGH CARDINALITY]" if col.get("is_high_cardinality") else ""

                col_line = f"      - {col['column_name']}: {col['full_data_type']} {nullable}"

                if col.get("actual_max_length"):
                    col_line += f" (actual max: {col['actual_max_length']})"

                col_line += f" | distinct: {col.get('distinct_count', 0)}"
                col_line += high_card

                summary_lines.append(col_line)

                # Add sample values for low cardinality columns
                if col.get("sample_values") and len(col["sample_values"]) <= 10:
                    samples = [s["value"][:50] for s in col["sample_values"][:5]]
                    summary_lines.append(f"        Top values: {', '.join(samples)}")

        return "\n".join(summary_lines)

    async def analyze(self) -> dict[str, Any]:
        """Perform complete enhanced schema analysis"""
        print(f"\n{'='*70}")
        print("MS SQL Schema Analysis v2 (Enhanced NL2SQL)")
        print(f"{'='*70}")
        print(f"Database: {self.database}")
        print(f"Schema: {self.schema}")
        print(f"{'='*70}")

        self.connect()

        try:
            # Get all tables
            tables = self.get_tables()
            print(f"\nFound {len(tables)} tables")

            # Analyze each table
            table_metadata = []
            for table_name in tables:
                metadata = self.get_table_metadata(table_name)
                table_metadata.append(metadata)

            # Build initial schema metadata
            schema_metadata = {
                "database": self.database,
                "schema": self.schema,
                "analyzed_at": datetime.now().isoformat(),
                "analyzer_version": "2.0",
                "tables": table_metadata,
                "table_count": len(table_metadata),
                "total_rows": sum(t["row_count"] for t in table_metadata),
                "high_cardinality_threshold": self.high_cardinality_threshold,
            }

            # Get LLM analysis
            llm_analysis = await self.analyze_with_llm(schema_metadata)

            # Combine metadata with LLM analysis
            final_output = {
                **schema_metadata,
                "llm_analysis": llm_analysis,
            }

            return final_output

        finally:
            self.disconnect()


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Analyze MS SQL schema with enhanced NL2SQL recommendations (v2)")
    parser.add_argument("--host", default=os.getenv("MSSQL_HOST", "127.0.0.1"), help="MS SQL host (default: 127.0.0.1)")
    parser.add_argument(
        "--port", type=int, default=int(os.getenv("MSSQL_PORT", "1433")), help="MS SQL port (default: 1433)"
    )
    parser.add_argument(
        "--database", default=os.getenv("RAW_DATA_DB_NAME", "raw_data_db"), help="Database name (default: raw_data_db)"
    )
    parser.add_argument("--username", default=os.getenv("MSSQL_USERNAME", "sa"), help="Database username (default: sa)")
    parser.add_argument(
        "--password",
        default=os.getenv("MSSQL_SA_PASSWORD"),
        help="Database password (default from env: MSSQL_SA_PASSWORD)",
    )
    parser.add_argument("--schema", default="seed_data_raw", help="Schema name to analyze (default: seed_data_raw)")
    parser.add_argument("--output", help="Output JSON file path (default: print to stdout)")
    parser.add_argument(
        "--litellm-url",
        default=os.getenv("LITELLM_BASE_URL", "http://localhost:4000"),
        help="LiteLLM base URL (default: http://localhost:4000)",
    )
    parser.add_argument(
        "--litellm-key",
        default=os.getenv("LITELLM_MASTER_KEY"),
        help="LiteLLM master key (default from env: LITELLM_MASTER_KEY)",
    )
    parser.add_argument(
        "--model", default=os.getenv("LITELLM_CHAT_MODEL", "gpt-4.1"), help="Chat model name (default: gpt-4.1)"
    )
    parser.add_argument(
        "--high-cardinality-threshold",
        type=int,
        default=200,
        help="Threshold for high cardinality detection (default: 200)",
    )

    args = parser.parse_args()

    # Validate required arguments
    if not args.password:
        print("❌ Error: Database password is required (--password or MSSQL_SA_PASSWORD)")
        sys.exit(1)

    if not args.litellm_key:
        print("❌ Error: LiteLLM master key is required (--litellm-key or LITELLM_MASTER_KEY)")
        sys.exit(1)

    # Initialize LiteLLM client
    litellm_client = LiteLLMClient(
        base_url=args.litellm_url,
        master_key=args.litellm_key,
        model=args.model,
    )

    # Initialize analyzer
    analyzer = MSSQLSchemaAnalyzerV2(
        host=args.host,
        port=args.port,
        database=args.database,
        username=args.username,
        password=args.password,
        schema=args.schema,
        litellm_client=litellm_client,
        high_cardinality_threshold=args.high_cardinality_threshold,
    )

    try:
        # Perform analysis
        result = await analyzer.analyze()

        # Output results
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            print(f"\n{'='*70}")
            print("✅ Analysis complete!")
            print(f"📄 Output written to: {output_path}")
            print("   Analyzer version: 2.0")
            print(f"   Tables analyzed: {result['table_count']}")
            print(f"   Total rows: {result['total_rows']:,}")
            print(f"{'='*70}")
        else:
            # Print to stdout
            print(f"\n{'='*70}")
            print("Analysis Results:")
            print(f"{'='*70}\n")
            print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

    finally:
        await litellm_client.close()


if __name__ == "__main__":
    asyncio.run(main())
