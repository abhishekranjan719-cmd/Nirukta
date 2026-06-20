#!/bin/bash
set -e

# PostgreSQL Multi-Database Initialization Script
# Creates separate databases for Backend, Langfuse, and LiteLLM with isolated users

echo "========================================="
echo "PostgreSQL Multi-Database Initialization"
echo "========================================="

# Function to create database and user
create_database() {
    local db_name=$1
    local db_user=$2
    local db_password=$3

    echo ""
    echo ">>> Creating database: $db_name"
    echo ">>> Creating user: $db_user"

    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        -- Create user if not exists
        DO \$\$
        BEGIN
            IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$db_user') THEN
                CREATE USER $db_user WITH PASSWORD '$db_password';
                RAISE NOTICE 'User $db_user created successfully';
            ELSE
                RAISE NOTICE 'User $db_user already exists';
            END IF;
        END
        \$\$;

        -- Create database if not exists
        SELECT 'CREATE DATABASE $db_name OWNER $db_user ENCODING ''UTF8'' LC_COLLATE ''en_US.UTF-8'' LC_CTYPE ''en_US.UTF-8'' TEMPLATE template0'
        WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$db_name')\gexec

        -- Grant privileges
        GRANT ALL PRIVILEGES ON DATABASE $db_name TO $db_user;

        -- Connect to new database and grant schema privileges
        \c $db_name
        GRANT ALL ON SCHEMA public TO $db_user;
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $db_user;
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $db_user;

        -- Back to default database
        \c $POSTGRES_DB
EOSQL

    echo "✅ Database $db_name created successfully with user $db_user"
}

# Main execution
echo ""
echo "Starting database creation..."
echo ""

# Database 1: Backend API
create_database "${MAIN_DB_NAME:-main_db}" "${MAIN_DB_USER:-main_user}" "${MAIN_DB_PASSWORD:-main_password}"

# Database 2: Langfuse
create_database "${LANGFUSE_DB_NAME:-langfuse}" "${LANGFUSE_DB_USER:-langfuse}" "${LANGFUSE_DB_PASSWORD:-langfuse_password}"

# Database 3: LiteLLM
create_database "${LITELLM_DB_NAME:-litellm}" "${LITELLM_DB_USER:-litellm}" "${LITELLM_DB_PASSWORD:-litellm_password}"

# Database 4: LangGraph (Agent Memory & Checkpointing)
create_database "${LANGGRAPH_DB_NAME:-langgraph}" "${LANGGRAPH_DB_USER:-langgraph}" "${LANGGRAPH_DB_PASSWORD:-langgraph_password_123}"

echo ""
echo "========================================="
echo "✅ All databases created successfully!"
echo "========================================="
echo ""
echo "Database Summary:"
echo "  1. ${MAIN_DB_NAME:-main_db} (user: ${MAIN_DB_USER:-main_user})"
echo "  2. ${LANGFUSE_DB_NAME:-langfuse} (user: ${LANGFUSE_DB_USER:-langfuse})"
echo "  3. ${LITELLM_DB_NAME:-litellm} (user: ${LITELLM_DB_USER:-litellm})"
echo "  4. ${LANGGRAPH_DB_NAME:-langgraph} (user: ${LANGGRAPH_DB_USER:-langgraph})"
echo ""
echo "PostgreSQL initialization complete!"
echo "========================================="
