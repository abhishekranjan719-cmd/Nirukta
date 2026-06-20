#!/usr/bin/env python3
"""
MS SQL Server Multi-Database Initialization Script
Creates separate databases for data storage with isolated logins/users

Requirements:
    pip install pyodbc

Usage:
    python 01-create-databases.py

Environment Variables:
    MSSQL_SA_PASSWORD: SA password (required)
    MSSQL_HOST: Server host (default: 127.0.0.1)
    MSSQL_PORT: Server port (default: 1433)

    # Database configurations (optional, with defaults)
    RAW_DATA_DB_NAME: Raw data database name
    RAW_DATA_DB_USER: Raw data user
    RAW_DATA_DB_PASSWORD: Raw data password
"""

import os
import sys

import pyodbc


class MSSQLInitializer:
    """MS SQL Server database initialization handler"""

    def __init__(self):
        """Initialize with configuration from environment variables"""
        # Connection settings
        self.host = os.getenv("MSSQL_HOST", "127.0.0.1")
        self.port = os.getenv("MSSQL_PORT", "1433")
        self.sa_password = os.getenv("MSSQL_SA_PASSWORD")

        if not self.sa_password:
            raise ValueError("MSSQL_SA_PASSWORD environment variable is required")

        # Database configurations with defaults
        self.databases = [
            {
                "db_name": os.getenv("RAW_DATA_DB_NAME", "raw_data_db"),
                "db_user": os.getenv("RAW_DATA_DB_USER", "raw_data_user"),
                "db_password": os.getenv("RAW_DATA_DB_PASSWORD", "RawData@123"),
            },
        ]

    def get_connection_string(self, database: str = "master") -> str:
        """
        Build MS SQL connection string with proper encoding for special characters.

        Args:
            database: Database name to connect to

        Returns:
            Connection string for pyodbc
        """
        # Using Trusted_Connection=no and explicitly providing credentials
        # Driver name might vary: "ODBC Driver 17 for SQL Server" or "ODBC Driver 18 for SQL Server"
        conn_str = (
            f"DRIVER={{SQL Server}};"
            f"SERVER={self.host},{self.port};"
            f"DATABASE={database};"
            f"UID=sa;"
            f"PWD={self.sa_password};"
            f"TrustServerCertificate=yes;"  # For local development
        )
        return conn_str

    def create_database(self, db_name: str, db_user: str, db_password: str) -> None:
        """
        Create database, login, user, and grant permissions.

        Args:
            db_name: Name of the database to create
            db_user: Username for the database
            db_password: Password for the user
        """
        print(f"\n>>> Creating database: {db_name}")
        print(f">>> Creating login/user: {db_user}")

        conn_str = self.get_connection_string("master")

        try:
            # Step 1: Create DATABASE first (must be done in isolation)
            print(f"    - Creating database '{db_name}'...")

            # Connect and check if database exists
            conn = pyodbc.connect(conn_str, autocommit=True)
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM sys.databases WHERE name = ?", (db_name,))
            db_exists = cursor.fetchone()
            cursor.close()
            conn.close()

            if db_exists:
                print(f"    [WARN]  Database '{db_name}' already exists, skipping creation")
            else:
                # CREATE DATABASE in a fresh connection with NO other statements
                conn_db = pyodbc.connect(conn_str)
                conn_db.autocommit = True  # Set autocommit explicitly
                cursor_db = conn_db.cursor()

                try:
                    cursor_db.execute(f"CREATE DATABASE [{db_name}]")
                    print(f"    [OK] Database '{db_name}' created")
                except pyodbc.Error as e:
                    if "already exists" in str(e):
                        print(f"    [WARN]  Database '{db_name}' already exists")
                    else:
                        raise
                finally:
                    cursor_db.close()
                    conn_db.close()

            # Step 2: Create LOGIN (server-level)
            print(f"    - Creating login '{db_user}'...")
            conn = pyodbc.connect(conn_str, autocommit=True)
            cursor = conn.cursor()

            try:
                # Check if login exists
                cursor.execute("SELECT name FROM sys.server_principals WHERE name = ?", (db_user,))
                if cursor.fetchone():
                    print(f"    [WARN]  Login '{db_user}' already exists, skipping creation")
                else:
                    cursor.execute(f"CREATE LOGIN [{db_user}] WITH PASSWORD = '{db_password}'")
                    print(f"    [OK] Login '{db_user}' created")
            except pyodbc.Error as e:
                if "already exists" in str(e):
                    print(f"    [WARN]  Login '{db_user}' already exists")
                else:
                    raise
            finally:
                cursor.close()
                conn.close()

            # Step 3: Create USER and grant permissions (in the new database)
            print("    - Creating user and granting permissions...")
            conn_str = self.get_connection_string(db_name)
            conn = pyodbc.connect(conn_str, autocommit=True)
            cursor = conn.cursor()

            try:
                # Check if user exists
                cursor.execute("SELECT name FROM sys.database_principals WHERE name = ?", (db_user,))
                if cursor.fetchone():
                    print(f"    [WARN]  User '{db_user}' already exists in database")
                else:
                    cursor.execute(f"CREATE USER [{db_user}] FOR LOGIN [{db_user}]")
                    print(f"    [OK] User '{db_user}' created in database")
            except pyodbc.Error as e:
                if "already exists" in str(e):
                    print(f"    [WARN]  User '{db_user}' already exists in database")
                else:
                    raise

            # Grant db_owner role (full permissions on database)
            cursor.execute(f"ALTER ROLE db_owner ADD MEMBER [{db_user}]")
            print(f"    [OK] Granted db_owner role to '{db_user}'")

            cursor.close()
            conn.close()

            print(f"[OK] Database {db_name} created successfully with user {db_user}")

        except pyodbc.Error as e:
            print(f"[ERROR] Error creating database {db_name}: {e}")
            raise

    def test_connection(self) -> bool:
        """
        Test connection to MS SQL Server.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            conn_str = self.get_connection_string("master")
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]
            print("[OK] Connected to MS SQL Server")
            print(f"   Version: {version.split(chr(10))[0]}")  # First line only
            cursor.close()
            conn.close()
            return True
        except pyodbc.Error as e:
            print(f"[ERROR] Connection failed: {e}")
            return False

    def run(self) -> None:
        """Execute the initialization process"""
        print("=" * 60)
        print("MS SQL Server Multi-Database Initialization")
        print("=" * 60)
        print(f"\nServer: {self.host}:{self.port}")
        print("Connecting as: sa")

        # Test connection first
        print("\nTesting connection...")
        if not self.test_connection():
            print("\n[ERROR] Failed to connect to MS SQL Server")
            print("   Please ensure:")
            print("   1. MS SQL Server is running")
            print("   2. MSSQL_SA_PASSWORD is correct")
            print("   3. Server is accessible at {self.host}:{self.port}")
            sys.exit(1)

        print("\n" + "=" * 60)
        print("Creating databases...")
        print("=" * 60)

        # Create all databases
        for db_config in self.databases:
            try:
                self.create_database(db_config["db_name"], db_config["db_user"], db_config["db_password"])
            except Exception as e:
                print(f"\n[ERROR] Failed to create database {db_config['db_name']}: {e}")
                continue

        print("\n" + "=" * 60)
        print("[OK] All databases created successfully!")
        print("=" * 60)

        print("\nDatabase Summary:")
        for idx, db_config in enumerate(self.databases, 1):
            print(f"  {idx}. {db_config['db_name']} (user: {db_config['db_user']})")

        print("\nMS SQL Server initialization complete!")
        print("=" * 60)


def main():
    """Main entry point"""
    try:
        initializer = MSSQLInitializer()
        initializer.run()
    except ValueError as e:
        print(f"[ERROR] Configuration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
