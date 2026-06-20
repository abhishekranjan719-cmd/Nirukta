# Environment Variables Documentation

Complete reference for all environment variables used in the consolidated infrastructure.

## Table of Contents

- [Overview](#overview)
- [Mode Configuration](#mode-configuration)
- [Backend Service](#backend-service)
- [Engine Service](#engine-service)
- [Engine LLM Configuration](#engine-llm-configuration)
- [Agent Configuration (QnA Agent)](#agent-configuration-qna-agent)
- [PostgreSQL Database](#postgresql-database)
- [LangGraph Memory System](#langgraph-memory-system)
- [Redis Stack](#redis-stack)
- [Langfuse Observability](#langfuse-observability)
- [LiteLLM Proxy](#litellm-proxy)
- [Azure OpenAI](#azure-openai)
- [Azure AI (Cohere Rerank)](#azure-ai-cohere-rerank)
- [ClickHouse](#clickhouse)
- [MinIO Object Storage](#minio-object-storage)
- [Frontend](#frontend)
- [Required vs Optional](#required-vs-optional)
- [Production Security](#production-security)

---

## Overview

All environment variables are managed through:
1. `.env` file in project root (single source of truth)
2. `configs/settings.py` (Pydantic Settings for type-safe loading)
3. Service-specific configs (`backend/app/config.py`, `engine/app/config.py`)

**Configuration Flow:**
```
.env → Pydantic Settings → Service Config → Application Code
```

---

## Mode Configuration

### MODE

**Description:** Environment mode controlling service behavior
**Type:** Enum (`local` or `dev`)
**Default:** `local`
**Required:** No

**Values:**
- `local`: Development mode with hot reload enabled
- `dev`: Production-like mode with hot reload disabled

**Example:**
```bash
MODE=local
```

**Impact:**
- Controls auto-reload for backend and engine services
- Affects logging verbosity
- Determines configuration file loading behavior

---

## Backend Service

### BACKEND_ENGINE_URL

**Description:** URL to engine service for backend API calls
**Type:** URL string
**Default:** `http://localhost:8001`
**Required:** Yes

**Docker Compose:**
```bash
BACKEND_ENGINE_URL=http://engine:8001
```

**Local Development:**
```bash
BACKEND_ENGINE_URL=http://localhost:8001
```

### BACKEND_CORS_ORIGINS

**Description:** Allowed CORS origins for backend API (JSON array)
**Type:** JSON string array
**Default:** `["http://localhost:5173"]`
**Required:** Yes

**Example:**
```bash
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
```

**Production:**
```bash
BACKEND_CORS_ORIGINS=["https://yourdomain.com","https://app.yourdomain.com"]
```

### BACKEND_HOST

**Description:** Backend server host address
**Type:** String (IP or hostname)
**Default:** `0.0.0.0`
**Required:** No

**Note:** `0.0.0.0` binds to all interfaces (required for Docker)

### BACKEND_PORT

**Description:** Backend server port
**Type:** Integer
**Default:** `8000`
**Required:** No

### BACKEND_RELOAD

**Description:** Enable auto-reload on code changes
**Type:** Boolean
**Default:** `true` (overridden by MODE)
**Required:** No

**Note:** Automatically set to `false` when `MODE=dev`

---

## Engine Service

### ENGINE_CORS_ORIGINS

**Description:** Allowed CORS origins for engine API (JSON array)
**Type:** JSON string array
**Default:** `["http://localhost:8000"]`
**Required:** Yes

**Important:** Engine should only accept requests from backend

**Example:**
```bash
ENGINE_CORS_ORIGINS=["http://localhost:8000"]
```

**Docker Compose:**
```bash
ENGINE_CORS_ORIGINS=["http://backend:8000"]
```

### ENGINE_HOST

**Description:** Engine server host address
**Type:** String (IP or hostname)
**Default:** `0.0.0.0`
**Required:** No

### ENGINE_PORT

**Description:** Engine server port
**Type:** Integer
**Default:** `8001`
**Required:** No

### ENGINE_RELOAD

**Description:** Enable auto-reload on code changes
**Type:** Boolean
**Default:** `true` (overridden by MODE)
**Required:** No

**Note:** Automatically set to `false` when `MODE=dev`

---

## Engine LLM Configuration

Configuration for LLM behavior in the engine service (temperature, timeout, streaming).

### ENGINE_LLM_TEMPERATURE

**Description:** LLM temperature setting for response generation
**Type:** Float (0.0 to 2.0)
**Default:** `0.7`
**Required:** No

**Temperature Guide:**
- `0.0`: Deterministic, focused (best for factual tasks)
- `0.7`: Balanced creativity and consistency (default)
- `1.0`: More creative and varied responses
- `2.0`: Highly creative, less predictable

**Example:**
```bash
# More deterministic for factual responses
ENGINE_LLM_TEMPERATURE=0.3

# More creative for brainstorming
ENGINE_LLM_TEMPERATURE=1.2
```

**Impact:**
- Affects both workflow and agent orchestration modes
- Lower values: More consistent, focused outputs
- Higher values: More diverse, creative outputs

### ENGINE_LLM_TIMEOUT

**Description:** HTTP timeout for LLM API requests
**Type:** Integer (seconds)
**Default:** `60`
**Required:** No

**Example:**
```bash
# Longer timeout for slower models or complex requests
ENGINE_LLM_TIMEOUT=120

# Shorter timeout for faster models
ENGINE_LLM_TIMEOUT=30
```

**Impact:**
- Applies to LiteLLM proxy and Azure OpenAI direct calls
- Requests exceeding timeout will fail with timeout error
- Consider model speed and request complexity when setting

### ENGINE_LLM_STREAMING

**Description:** Enable/disable streaming mode for LLM responses
**Type:** Boolean
**Default:** `false`
**Required:** No

**Example:**
```bash
# Enable streaming for real-time response display
ENGINE_LLM_STREAMING=true

# Disable streaming (get complete response at once)
ENGINE_LLM_STREAMING=false
```

**Note:** Frontend must support streaming to use this feature effectively

### ENGINE_HTTP_SSL_VERIFY

**Description:** Enable/disable SSL certificate verification for HTTP clients
**Type:** Boolean
**Default:** `false`
**Required:** No

**Example:**
```bash
# Development (self-signed certificates)
ENGINE_HTTP_SSL_VERIFY=false

# Production (proper SSL certificates)
ENGINE_HTTP_SSL_VERIFY=true
```

**Security Warning:**
- Set to `false` only in local development with self-signed certs
- **Always** set to `true` in production for security
- Disabling SSL verification makes connections vulnerable to MITM attacks

---

## Agent Configuration (QnA Agent)

Configuration for LangGraph ReAct agent behavior (conversation summarization, memory management).

### AGENT_MAX_MESSAGES_BEFORE_SUMMARY

**Description:** Maximum messages before triggering conversation summarization
**Type:** Integer
**Default:** `10`
**Required:** No

**Example:**
```bash
# Summarize sooner for shorter context
AGENT_MAX_MESSAGES_BEFORE_SUMMARY=5

# Summarize later for longer context
AGENT_MAX_MESSAGES_BEFORE_SUMMARY=20
```

**Impact:**
- Controls when long conversations are summarized
- Lower values: More frequent summarization (less context)
- Higher values: Less frequent summarization (more context, more tokens)

**Recommendation:** 5-15 for most use cases

### AGENT_MESSAGES_TO_KEEP_AFTER_SUMMARY

**Description:** Number of recent messages to keep after summarization
**Type:** Integer
**Default:** `2`
**Required:** No

**Example:**
```bash
# Keep more recent context
AGENT_MESSAGES_TO_KEEP_AFTER_SUMMARY=5

# Aggressive pruning
AGENT_MESSAGES_TO_KEEP_AFTER_SUMMARY=1
```

**Impact:**
- Determines how much recent conversation remains after summarization
- Lower values: More aggressive context reduction
- Higher values: More recent context preserved

**Formula:** Final messages = summary + recent N messages

### AGENT_SUMMARY_MESSAGE_COUNT

**Description:** Number of recent messages to include in summary generation
**Type:** Integer
**Default:** `5`
**Required:** No

**Example:**
```bash
# Include more messages in summary
AGENT_SUMMARY_MESSAGE_COUNT=10

# Shorter summary from fewer messages
AGENT_SUMMARY_MESSAGE_COUNT=3
```

**Impact:**
- Controls how many recent messages are analyzed for summary
- Higher values: More comprehensive summary
- Lower values: Faster summary generation

### AGENT_SUMMARY_MAX_LENGTH

**Description:** Maximum character length for generated summary
**Type:** Integer
**Default:** `200`
**Required:** No

**Example:**
```bash
# Longer, more detailed summaries
AGENT_SUMMARY_MAX_LENGTH=500

# Shorter, concise summaries
AGENT_SUMMARY_MAX_LENGTH=100
```

**Impact:**
- Truncates summary content at specified character count
- Helps control token usage in subsequent agent calls
- Balance between context retention and efficiency

---

## PostgreSQL Database

### POSTGRES_USER

**Description:** PostgreSQL superuser username
**Type:** String
**Default:** `postgres`
**Required:** Yes

**Security:** Change in production!

### POSTGRES_PASSWORD

**Description:** PostgreSQL superuser password
**Type:** String
**Default:** `postgres`
**Required:** Yes

**Security:** Use strong password in production!

### POSTGRES_DB

**Description:** Default database name
**Type:** String
**Default:** `postgres`
**Required:** Yes

---

### Main Database Configuration

### MAIN_DB_NAME

**Description:** Main application database name
**Type:** String
**Default:** `main_db`
**Required:** Yes

### MAIN_DB_USER

**Description:** Main application database user
**Type:** String
**Default:** `main_user`
**Required:** Yes

### MAIN_DB_PASSWORD

**Description:** Main application database password
**Type:** String
**Default:** (none - must be set in `.env`)
**Required:** Yes

**Security:** Use strong password in production!

**Connection URL:** `postgresql://main_user:<PASSWORD>@postgres:5432/main_db`

---

### Langfuse Database Configuration

### LANGFUSE_DB_NAME

**Description:** Langfuse database name
**Type:** String
**Default:** `langfuse`
**Required:** Yes (if using Langfuse)

### LANGFUSE_DB_USER

**Description:** Langfuse database user
**Type:** String
**Default:** `langfuse`
**Required:** Yes (if using Langfuse)

### LANGFUSE_DB_PASSWORD

**Description:** Langfuse database password
**Type:** String
**Default:** (none - must be set in `.env`)
**Required:** Yes (if using Langfuse)

**Security:** Use strong password in production!

**Connection URL:** `postgresql://langfuse:<PASSWORD>@postgres:5432/langfuse`

---

### LiteLLM Database Configuration

### LITELLM_DB_NAME

**Description:** LiteLLM database name
**Type:** String
**Default:** `litellm`
**Required:** Yes (if using LiteLLM)

### LITELLM_DB_USER

**Description:** LiteLLM database user
**Type:** String
**Default:** `litellm`
**Required:** Yes (if using LiteLLM)

### LITELLM_DB_PASSWORD

**Description:** LiteLLM database password
**Type:** String
**Default:** (none - must be set in `.env`)
**Required:** Yes (if using LiteLLM)

**Security:** Use strong password in production!

**Connection URL:** `postgresql://litellm:<PASSWORD>@postgres:5432/litellm`

---

### LangGraph Database Configuration

### LANGGRAPH_DB_NAME

**Description:** LangGraph database name (for agent memory and checkpointing)
**Type:** String
**Default:** `langgraph`
**Required:** Yes (if using LangGraph agent)

### LANGGRAPH_DB_USER

**Description:** LangGraph database user
**Type:** String
**Default:** `langgraph`
**Required:** Yes (if using LangGraph agent)

### LANGGRAPH_DB_PASSWORD

**Description:** LangGraph database password
**Type:** String
**Default:** `langgraph_password`
**Required:** Yes (if using LangGraph agent)

**Security:** Use strong password in production!

**Connection URL:** `postgresql://langgraph:langgraph_password@postgres:5432/langgraph`

**Purpose:**
- Stores conversation checkpoints for agent state persistence
- Enables multi-turn conversations with memory
- Provides conversation history across sessions

---

## LangGraph Memory System

Configuration for LangGraph agent memory persistence and message management.

### LANGGRAPH_MEMORY_ENABLED

**Description:** Enable/disable LangGraph memory system
**Type:** Boolean
**Default:** `true`
**Required:** No

**Example:**
```bash
# Enable persistent conversation memory
LANGGRAPH_MEMORY_ENABLED=true

# Disable memory (stateless agent)
LANGGRAPH_MEMORY_ENABLED=false
```

**Impact:**
- When enabled: Conversations persist across requests using PostgreSQL checkpointing
- When disabled: Each request is stateless (no conversation history)
- Requires `LANGGRAPH_DB_*` configuration when enabled

**Related Documentation:** See `docs/LANGGRAPH_MEMORY.md` for implementation details

### LANGGRAPH_MESSAGE_TRIM_ENABLED

**Description:** Enable/disable automatic message trimming
**Type:** Boolean
**Default:** `true`
**Required:** No

**Example:**
```bash
# Enable message trimming to manage context window
LANGGRAPH_MESSAGE_TRIM_ENABLED=true

# Disable trimming (keep all messages)
LANGGRAPH_MESSAGE_TRIM_ENABLED=false
```

**Impact:**
- Prevents conversation history from exceeding context window limits
- Reduces token usage in long conversations
- Maintains system messages while trimming older user/assistant messages

**Recommendation:** Keep enabled for production use

### LANGGRAPH_MESSAGE_TRIM_KEEP_LAST

**Description:** Number of recent messages to keep when trimming
**Type:** Integer
**Default:** `5`
**Required:** No

**Example:**
```bash
# Keep more recent messages (longer context)
LANGGRAPH_MESSAGE_TRIM_KEEP_LAST=10

# Keep fewer messages (shorter context, lower cost)
LANGGRAPH_MESSAGE_TRIM_KEEP_LAST=3
```

**Impact:**
- Controls context window size for LangGraph agent
- Higher values: More context, higher token costs
- Lower values: Less context, lower token costs

**Balance:** Context retention vs. cost efficiency

**Recommendation:** 3-10 for most use cases

### LANGGRAPH_MESSAGE_TRIM_MAX_TOKENS

**Description:** Maximum token limit for conversation history (future use)
**Type:** Integer
**Default:** `4000`
**Required:** No

**Example:**
```bash
# Allow more tokens in context
LANGGRAPH_MESSAGE_TRIM_MAX_TOKENS=8000

# Stricter token limit
LANGGRAPH_MESSAGE_TRIM_MAX_TOKENS=2000
```

**Status:** Configured but not yet implemented in trimming logic

**Future Use:** Token-based trimming (alternative to message-count-based)

---

## Redis Stack

### REDIS_HOST

**Description:** Redis server hostname
**Type:** String
**Default:** `redis-stack`
**Required:** Yes

### REDIS_PORT

**Description:** Redis server port
**Type:** Integer
**Default:** `6379`
**Required:** No

### REDIS_PASSWORD

**Description:** Redis authentication password
**Type:** String
**Default:** `""` (empty, no auth)
**Required:** No

**Security:** Set password in production!

**Example:**
```bash
REDIS_PASSWORD=your_secure_redis_password
```

### REDIS_MAX_MEMORY

**Description:** Maximum memory allocation for Redis
**Type:** String (with unit)
**Default:** `1024mb`
**Required:** No

**Example:**
```bash
REDIS_MAX_MEMORY=2048mb
```

**Connection URLs:**
- Main: `redis://redis-stack:6379/0`
- Langfuse: `redis://redis-stack:6379/1`
- LiteLLM: `redis://redis-stack:6379/2`

---

## Langfuse Observability

### LANGFUSE_PUBLIC_KEY

**Description:** Langfuse API public key
**Type:** String
**Default:** `""` (empty)
**Required:** Yes (to enable Langfuse)

**Generate:** Create project in Langfuse UI → Get API keys

**Example:**
```bash
LANGFUSE_PUBLIC_KEY=pk-lf-1234567890abcdef
```

### LANGFUSE_SECRET_KEY

**Description:** Langfuse API secret key
**Type:** String
**Default:** `""` (empty)
**Required:** Yes (to enable Langfuse)

**Security:** Keep secret! Never commit to version control

**Example:**
```bash
LANGFUSE_SECRET_KEY=sk-lf-1234567890abcdef
```

### LANGFUSE_HOST

**Description:** Langfuse server URL
**Type:** URL string
**Default:** `http://langfuse-web:3000`
**Required:** Yes

**Docker Compose:**
```bash
LANGFUSE_HOST=http://langfuse-web:3000
```

**Cloud:**
```bash
LANGFUSE_HOST=https://cloud.langfuse.com
```

---

### Langfuse Encryption Keys

**Important:** These must be exactly 64 hex characters (256 bits)

### LANGFUSE_NEXTAUTH_SECRET

**Description:** NextAuth.js session encryption secret
**Type:** String (64 hex chars)
**Default:** `""` (empty)
**Required:** Yes

**Generate:**
```bash
openssl rand -hex 32
```

**Example:**
```bash
LANGFUSE_NEXTAUTH_SECRET=a1b2c3d4e5f6789012345678901234567890123456789012345678901234567890
```

### LANGFUSE_ENCRYPTION_KEY

**Description:** Langfuse data encryption key
**Type:** String (64 hex chars)
**Default:** `""` (empty)
**Required:** Yes

**Generate:**
```bash
openssl rand -hex 32
```

**Security:** Never change after initialization (data loss!)

### LANGFUSE_SALT

**Description:** Password hashing salt
**Type:** String (64 hex chars)
**Default:** `""` (empty)
**Required:** Yes

**Generate:**
```bash
openssl rand -hex 32
```

**Security:** Never change after initialization!

---

### Langfuse Initialization

### LANGFUSE_INIT_ORG_ID

**Description:** Initial organization ID
**Type:** String
**Default:** `zuna-org`
**Required:** No

### LANGFUSE_INIT_ORG_NAME

**Description:** Initial organization name
**Type:** String
**Default:** `Zuna Organization`
**Required:** No

### LANGFUSE_INIT_PROJECT_ID

**Description:** Initial project ID
**Type:** String
**Default:** `zuna-project`
**Required:** No

### LANGFUSE_INIT_PROJECT_NAME

**Description:** Initial project name
**Type:** String
**Default:** `Zuna Project`
**Required:** No

### LANGFUSE_INIT_PROJECT_PUBLIC_KEY

**Description:** Initial project public API key
**Type:** String
**Default:** `""` (auto-generated)
**Required:** No

### LANGFUSE_INIT_PROJECT_SECRET_KEY

**Description:** Initial project secret API key
**Type:** String
**Default:** `""` (auto-generated)
**Required:** No

### LANGFUSE_INIT_USER_EMAIL

**Description:** Initial admin user email
**Type:** String (email)
**Default:** `admin@example.com`
**Required:** Yes

**Change in production!**

### LANGFUSE_INIT_USER_NAME

**Description:** Initial admin user name
**Type:** String
**Default:** `Admin`
**Required:** No

### LANGFUSE_INIT_USER_PASSWORD

**Description:** Initial admin user password
**Type:** String
**Default:** `admin123`
**Required:** Yes

**Security:** Change immediately after first login!

---

## LiteLLM Proxy

### LITELLM_MASTER_KEY

**Description:** LiteLLM API master key for authentication
**Type:** String
**Default:** `sk-1234`
**Required:** Yes

**Security:** Use strong key in production!

**Format:** Must start with `sk-`

**Example:**
```bash
LITELLM_MASTER_KEY=sk-1234567890abcdef
```

**Usage:**
```bash
curl -H "Authorization: Bearer sk-1234567890abcdef" http://localhost:4000/health
```

### LITELLM_SALT_KEY

**Description:** LiteLLM salt for key hashing
**Type:** String
**Default:** `sk-salt-1234`
**Required:** Yes

**Security:** Use strong salt in production!

### LITELLM_BASE_URL

**Description:** LiteLLM proxy server URL
**Type:** URL string
**Default:** `http://litellm:4000`
**Required:** Yes

**Docker Compose:**
```bash
LITELLM_BASE_URL=http://litellm:4000
```

**Local:**
```bash
LITELLM_BASE_URL=http://localhost:4000
```

### LITELLM_UI_USERNAME

**Description:** LiteLLM admin UI username
**Type:** String
**Default:** `admin`
**Required:** No

**Change in production!**

### LITELLM_UI_PASSWORD

**Description:** LiteLLM admin UI password
**Type:** String
**Default:** `admin123`
**Required:** No

**Security:** Change in production!

---

## Azure OpenAI

### AZURE_OPENAI_ENDPOINT

**Description:** Azure OpenAI service endpoint URL
**Type:** URL string
**Default:** `""` (empty)
**Required:** Yes (to use Azure OpenAI)

**Example:**
```bash
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
```

**Note:** Must end with `/`

### AZURE_OPENAI_API_KEY

**Description:** Azure OpenAI API key
**Type:** String
**Default:** `""` (empty)
**Required:** Yes (to use Azure OpenAI)

**Security:** Keep secret! Never commit to version control

**Example:**
```bash
AZURE_OPENAI_API_KEY=1234567890abcdef1234567890abcdef
```

**Get Key:** Azure Portal → Your OpenAI Resource → Keys and Endpoint

### AZURE_OPENAI_API_VERSION

**Description:** Azure OpenAI API version
**Type:** String (date format)
**Default:** `2025-01-01-preview`
**Required:** No

**Valid Versions:**
- `2025-01-01-preview` (latest)
- `2024-12-01-preview`
- `2024-10-21`
- `2024-08-01-preview`

**Example:**
```bash
AZURE_OPENAI_API_VERSION=2025-01-01-preview
```

---

## Azure AI (Cohere Rerank)

### AZURE_AI_API_BASE

**Description:** Azure AI Cohere rerank service base URL
**Type:** URL string
**Default:** `""` (empty)
**Required:** Yes (to use Cohere rerank)

**Example:**
```bash
AZURE_AI_API_BASE=https://Cohere-rerank-v3-5-xxxxx.eastus.models.ai.azure.com
```

### AZURE_AI_API_KEY

**Description:** Azure AI Cohere service API key
**Type:** String
**Default:** `""` (empty)
**Required:** Yes (to use Cohere rerank)

**Security:** Keep secret! Never commit to version control

**Example:**
```bash
AZURE_AI_API_KEY=abcdef1234567890abcdef1234567890
```

---

## ClickHouse

### CLICKHOUSE_USER

**Description:** ClickHouse admin username
**Type:** String
**Default:** `default`
**Required:** No

### CLICKHOUSE_PASSWORD

**Description:** ClickHouse admin password
**Type:** String
**Default:** (none - must be set in `.env`)
**Required:** Yes

**Security:** Use strong password in production!

### CLICKHOUSE_DB

**Description:** Default ClickHouse database
**Type:** String
**Default:** `default`
**Required:** No

---

## MinIO Object Storage

### MINIO_ROOT_USER

**Description:** MinIO admin username
**Type:** String
**Default:** `minioadmin`
**Required:** Yes

**Change in production!**

### MINIO_ROOT_PASSWORD

**Description:** MinIO admin password
**Type:** String
**Default:** `minioadmin123`
**Required:** Yes

**Security:** Use strong password in production! (min 8 chars)

### MINIO_ENDPOINT

**Description:** MinIO server endpoint
**Type:** URL string
**Default:** `http://minio:9000`
**Required:** No

### MINIO_PORT

**Description:** MinIO API port
**Type:** Integer
**Default:** `9000`
**Required:** No

### MINIO_CONSOLE_PORT

**Description:** MinIO console UI port
**Type:** Integer
**Default:** `9001`
**Required:** No

---

## Frontend

### VITE_BACKEND_URL

**Description:** Backend API URL for frontend
**Type:** URL string
**Default:** `http://localhost:8000`
**Required:** Yes

**Docker Compose:**
```bash
VITE_BACKEND_URL=http://localhost:8000
```

**Production:**
```bash
VITE_BACKEND_URL=https://api.yourdomain.com
```

**Note:** Vite env vars must start with `VITE_` to be exposed to browser

---

## Required vs Optional

### Critical (Required for Basic Operation)

Must be set for services to start:

```bash
# Mode
MODE=local

# Backend
BACKEND_ENGINE_URL=http://engine:8001
BACKEND_CORS_ORIGINS=["http://localhost:5173"]

# Engine
ENGINE_CORS_ORIGINS=["http://localhost:8000"]

# PostgreSQL
POSTGRES_PASSWORD=CHANGE_ME_POSTGRES_PASSWORD
MAIN_DB_PASSWORD=CHANGE_ME_MAIN_PASSWORD

# Frontend
VITE_BACKEND_URL=http://localhost:8000
```

### Langfuse (Required if using Langfuse)

```bash
# API Keys
LANGFUSE_PUBLIC_KEY=pk-lf-xxx
LANGFUSE_SECRET_KEY=sk-lf-xxx

# Encryption (must be 64 hex chars)
LANGFUSE_NEXTAUTH_SECRET=$(openssl rand -hex 32)
LANGFUSE_ENCRYPTION_KEY=$(openssl rand -hex 32)
LANGFUSE_SALT=$(openssl rand -hex 32)

# Database
LANGFUSE_DB_PASSWORD=CHANGE_ME_LANGFUSE_PASSWORD

# Initial User
LANGFUSE_INIT_USER_EMAIL=admin@example.com
LANGFUSE_INIT_USER_PASSWORD=CHANGE_ME_ADMIN_PASSWORD
```

### LiteLLM (Required if using LiteLLM)

```bash
# Authentication
LITELLM_MASTER_KEY=sk-1234567890abcdef

# Database
LITELLM_DB_PASSWORD=CHANGE_ME_LITELLM_PASSWORD
```

### Azure OpenAI (Required if using Azure OpenAI)

```bash
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_azure_openai_key
```

### Optional (With Defaults)

These have sensible defaults and don't need to be set:

- `BACKEND_HOST`, `BACKEND_PORT`, `ENGINE_HOST`, `ENGINE_PORT`
- `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`
- `LANGFUSE_HOST` (if using Docker Compose)
- `LITELLM_BASE_URL` (if using Docker Compose)
- All `*_INIT_*` variables (have defaults)

**Engine Configuration (With Sensible Defaults):**
- `ENGINE_LLM_TEMPERATURE` (default: 0.7)
- `ENGINE_LLM_TIMEOUT` (default: 60 seconds)
- `ENGINE_LLM_STREAMING` (default: false)
- `ENGINE_HTTP_SSL_VERIFY` (default: false for development)

**Agent Configuration (With Sensible Defaults):**
- `AGENT_MAX_MESSAGES_BEFORE_SUMMARY` (default: 10)
- `AGENT_MESSAGES_TO_KEEP_AFTER_SUMMARY` (default: 2)
- `AGENT_SUMMARY_MESSAGE_COUNT` (default: 5)
- `AGENT_SUMMARY_MAX_LENGTH` (default: 200)

**LangGraph Memory (With Sensible Defaults):**
- `LANGGRAPH_MEMORY_ENABLED` (default: true)
- `LANGGRAPH_MESSAGE_TRIM_ENABLED` (default: true)
- `LANGGRAPH_MESSAGE_TRIM_KEEP_LAST` (default: 5)
- `LANGGRAPH_MESSAGE_TRIM_MAX_TOKENS` (default: 4000)

---

## Production Security

### Security Checklist

**Before deploying to production:**

1. **Change All Default Passwords:**
   ```bash
   ✓ POSTGRES_PASSWORD
   ✓ MAIN_DB_PASSWORD
   ✓ LANGFUSE_DB_PASSWORD
   ✓ LITELLM_DB_PASSWORD
   ✓ LANGGRAPH_DB_PASSWORD
   ✓ REDIS_PASSWORD (set one!)
   ✓ CLICKHOUSE_PASSWORD
   ✓ MINIO_ROOT_PASSWORD
   ✓ LANGFUSE_INIT_USER_PASSWORD
   ✓ LITELLM_UI_PASSWORD
   ```

2. **Generate Strong Keys:**
   ```bash
   # Langfuse encryption keys (64 hex chars)
   openssl rand -hex 32  # Run 3 times for NEXTAUTH, ENCRYPTION, SALT

   # LiteLLM master key
   openssl rand -hex 16  # Prefix with sk-
   ```

3. **Change Default Usernames:**
   ```bash
   ✓ MAIN_DB_USER
   ✓ LANGFUSE_DB_USER
   ✓ LITELLM_DB_USER
   ✓ LANGFUSE_INIT_USER_EMAIL
   ✓ LITELLM_UI_USERNAME
   ✓ MINIO_ROOT_USER
   ```

4. **Update URLs for Production:**
   ```bash
   VITE_BACKEND_URL=https://api.yourdomain.com
   BACKEND_CORS_ORIGINS=["https://yourdomain.com"]
   ```

5. **Enable Redis Authentication:**
   ```bash
   REDIS_PASSWORD=your_strong_redis_password
   ```

6. **Review Exposure:**
   - Don't expose PostgreSQL, Redis, ClickHouse ports publicly
   - Use reverse proxy (nginx) for backend/frontend
   - Enable TLS/SSL for all services
   - Use Docker secrets instead of .env in production

### Password Strength Requirements

**Minimum Requirements:**
- Length: 12+ characters
- Complexity: Mix of uppercase, lowercase, numbers, symbols
- Uniqueness: Different password for each service

**Generate Secure Passwords:**
```bash
# Strong random password (32 chars)
openssl rand -base64 32

# Alphanumeric only (24 chars)
openssl rand -hex 12
```

### Environment File Security

**Development:**
```bash
# .env file permissions
chmod 600 .env

# Add to .gitignore
echo ".env" >> .gitignore
```

**Production:**
```bash
# Use Docker secrets
docker secret create postgres_password postgres_password.txt

# Or use environment variable injection
docker-compose --env-file /secure/path/.env up -d
```

### API Key Rotation

**Regular Rotation Schedule:**
- Langfuse keys: Every 90 days
- LiteLLM keys: Every 90 days
- Azure OpenAI keys: Every 180 days
- Database passwords: Every 180 days

**Rotation Procedure:**
1. Generate new keys
2. Update .env file
3. Restart affected services
4. Verify functionality
5. Revoke old keys

---

## Configuration Examples

### Minimal Local Development

```bash
# Mode
MODE=local

# Backend
BACKEND_ENGINE_URL=http://localhost:8001

# PostgreSQL
POSTGRES_PASSWORD=CHANGE_ME_POSTGRES_PASSWORD
MAIN_DB_PASSWORD=CHANGE_ME_MAIN_PASSWORD

# Frontend
VITE_BACKEND_URL=http://localhost:8000
```

### Full Stack with Observability

```bash
# Mode
MODE=local

# Backend
BACKEND_ENGINE_URL=http://engine:8001
BACKEND_CORS_ORIGINS=["http://localhost:5173"]

# Engine
ENGINE_CORS_ORIGINS=["http://localhost:8000"]

# PostgreSQL
POSTGRES_PASSWORD=CHANGE_ME_POSTGRES_PASSWORD
MAIN_DB_PASSWORD=CHANGE_ME_MAIN_PASSWORD
LANGFUSE_DB_PASSWORD=CHANGE_ME_LANGFUSE_PASSWORD
LITELLM_DB_PASSWORD=CHANGE_ME_LITELLM_PASSWORD
LANGGRAPH_DB_PASSWORD=CHANGE_ME_LANGGRAPH_PASSWORD

# LangGraph Memory
LANGGRAPH_MEMORY_ENABLED=true
LANGGRAPH_MESSAGE_TRIM_ENABLED=true
LANGGRAPH_MESSAGE_TRIM_KEEP_LAST=5

# Engine LLM Configuration
ENGINE_LLM_TEMPERATURE=0.7
ENGINE_LLM_TIMEOUT=60
ENGINE_HTTP_SSL_VERIFY=false

# Agent Configuration
AGENT_MAX_MESSAGES_BEFORE_SUMMARY=10
AGENT_MESSAGES_TO_KEEP_AFTER_SUMMARY=2

# Redis
REDIS_PASSWORD=redis_password_123

# Langfuse
LANGFUSE_PUBLIC_KEY=pk-lf-xxx
LANGFUSE_SECRET_KEY=sk-lf-xxx
LANGFUSE_NEXTAUTH_SECRET=$(openssl rand -hex 32)
LANGFUSE_ENCRYPTION_KEY=$(openssl rand -hex 32)
LANGFUSE_SALT=$(openssl rand -hex 32)
LANGFUSE_INIT_USER_EMAIL=admin@yourdomain.com
LANGFUSE_INIT_USER_PASSWORD=secure_password_123

# LiteLLM
LITELLM_MASTER_KEY=sk-1234567890abcdef

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_key

# Frontend
VITE_BACKEND_URL=http://localhost:8000
```

### Production Example

```bash
# Mode
MODE=dev

# Backend
BACKEND_ENGINE_URL=http://engine:8001
BACKEND_CORS_ORIGINS=["https://app.yourdomain.com"]

# Engine
ENGINE_CORS_ORIGINS=["http://backend:8000"]

# PostgreSQL (strong passwords)
POSTGRES_PASSWORD=xK9#mP2$vL7@nB5
MAIN_DB_PASSWORD=hR4&jF8*wQ3!zN6
LANGFUSE_DB_PASSWORD=pT5@gY9$kM2#xW7
LITELLM_DB_PASSWORD=vN3!bH8*mL4&jR9
LANGGRAPH_DB_PASSWORD=kP8@mN5$vR3!wH6

# LangGraph Memory (production settings)
LANGGRAPH_MEMORY_ENABLED=true
LANGGRAPH_MESSAGE_TRIM_ENABLED=true
LANGGRAPH_MESSAGE_TRIM_KEEP_LAST=10

# Engine LLM Configuration (production settings)
ENGINE_LLM_TEMPERATURE=0.5
ENGINE_LLM_TIMEOUT=90
ENGINE_HTTP_SSL_VERIFY=true

# Agent Configuration (production settings)
AGENT_MAX_MESSAGES_BEFORE_SUMMARY=15
AGENT_MESSAGES_TO_KEEP_AFTER_SUMMARY=3

# Redis (authentication enabled)
REDIS_PASSWORD=qW7$eR4@tY9#uI2

# Langfuse (production keys)
LANGFUSE_PUBLIC_KEY=pk-lf-production-key
LANGFUSE_SECRET_KEY=sk-lf-production-secret
LANGFUSE_NEXTAUTH_SECRET=a1b2c3d4... (64 hex chars)
LANGFUSE_ENCRYPTION_KEY=e5f6g7h8... (64 hex chars)
LANGFUSE_SALT=i9j0k1l2... (64 hex chars)
LANGFUSE_INIT_USER_EMAIL=admin@yourdomain.com
LANGFUSE_INIT_USER_PASSWORD=Strong!Pass123

# LiteLLM
LITELLM_MASTER_KEY=sk-production-master-key

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://prod-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=production_key

# Frontend
VITE_BACKEND_URL=https://api.yourdomain.com
```

---

## Validation

### Verify Settings Loading

**Backend:**
```bash
docker exec chat-backend python -c "
from app.config import settings
print(f'Backend Mode: {settings.mode}')
print(f'Engine URL: {settings.engine_url}')
print(f'PostgreSQL: {settings.postgres.main_database_url}')
print(f'Redis: {settings.redis.main_redis_url}')
print(f'Langfuse Enabled: {settings.langfuse.is_enabled}')
print(f'LiteLLM Enabled: {settings.litellm.is_enabled}')
"
```

**Engine:**
```bash
docker exec chat-engine python -c "
from app.config import settings
print(f'Engine Mode: {settings.mode}')
print(f'PostgreSQL: {settings.postgres.main_database_url}')
print(f'Azure OpenAI Enabled: {settings.azure_openai.is_enabled}')
"
```

### Check Environment Variables

```bash
# Inside container
docker exec chat-backend env | grep -E "BACKEND|POSTGRES|REDIS|LANGFUSE|LITELLM|AZURE"

# From host
docker exec chat-backend printenv BACKEND_ENGINE_URL
docker exec chat-backend printenv LANGFUSE_PUBLIC_KEY
```

---

**Last Updated:** 2026-01-03
**Version:** 1.1.0
**Changes:** Added Engine LLM Configuration, Agent Configuration, and LangGraph Memory System sections
