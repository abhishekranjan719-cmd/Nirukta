# Services Documentation

This document provides comprehensive information about all services in the consolidated infrastructure.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Service Inventory](#service-inventory)
- [Service Access](#service-access)
- [Infrastructure Layer](#infrastructure-layer)
- [Supporting Services](#supporting-services)
- [Observability & Gateway](#observability--gateway)
- [Application Layer](#application-layer)

---

## Architecture Overview

The application uses a **consolidated microservices architecture** with:

- **1 PostgreSQL instance** serving 3 logical databases
- **1 Redis Stack instance** serving 3 logical database numbers
- **Observability** via Langfuse for LLM tracing
- **LLM Gateway** via LiteLLM for unified AI model access
- **Full-stack** React frontend + FastAPI backend + FastAPI engine

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                         │
│                      http://localhost:5173                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                     BACKEND (FastAPI)                            │
│                      http://localhost:8000                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                     ENGINE (FastAPI)                             │
│                      http://localhost:8001                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
┌────────▼────────┐  ┌───────▼────────┐  ┌──────▼──────┐
│   LiteLLM       │  │   Langfuse     │  │ PostgreSQL  │
│   (Gateway)     │  │ (Observability)│  │  (3 DBs)    │
│   Port: 4000    │  │   Port: 3000   │  │ Port: 5432  │
└─────────────────┘  └────────────────┘  └─────────────┘
```

---

## Service Inventory

### Total Services: 12

| # | Service | Type | Status | Port(s) |
|---|---------|------|--------|---------|
| 1 | PostgreSQL | Database | ✅ Healthy | 5432 (localhost) |
| 2 | Redis Stack | Cache/Queue | ✅ Healthy | 6379 (localhost) |
| 3 | MSSQL | Database | ✅ Healthy | 1433 (localhost) |
| 4 | ClickHouse | Analytics DB | ✅ Healthy | 8123, 9000 (localhost) |
| 5 | MinIO | Object Storage | ✅ Healthy | 9090, 9091 (public) |
| 6 | SQLPad | SQL Editor | ✅ Healthy | 3010 (localhost) |
| 7 | Langfuse Web | Observability | ✅ Healthy | 3000 (public) |
| 8 | Langfuse Worker | Background Jobs | ✅ Running | 3030 (localhost) |
| 9 | LiteLLM | LLM Gateway | ✅ Healthy | 4000 (public) |
| 10 | Frontend | React UI | ✅ Running | 5173 (public) |
| 11 | Backend | FastAPI | ✅ Healthy | 8000 (public) |
| 12 | Engine | FastAPI | ✅ Healthy | 8001 (internal) |

---

## Service Access

### Public Services (Accessible from Host)

| Service | URL | Credentials | Purpose |
|---------|-----|-------------|---------|
| **Frontend** | http://localhost:5173 | - | Main application UI |
| **Backend API** | http://localhost:8000 | - | Backend REST API |
| **Backend Docs** | http://localhost:8000/docs | - | Swagger documentation |
| **Langfuse UI** | http://localhost:3000 | admin@example.com / (see `.env`) | LLM observability dashboard |
| **LiteLLM UI** | http://localhost:4000/ui | admin / (see `.env`) | LLM gateway dashboard |
| **MinIO Console** | http://localhost:9091 | See `.env` for credentials | S3 storage console |

### Localhost-Only Services

| Service | URL | Credentials | Purpose |
|---------|-----|-------------|---------|
| **PostgreSQL** | localhost:5432 | See `.env` file | Database access |
| **Redis** | localhost:6379 | No password | Cache access |
| **MSSQL** | localhost:1433 | sa / (see `.env`) | SQL Server access |
| **ClickHouse** | localhost:8123 | default / (see `.env`) | Analytics queries |
| **SQLPad** | http://localhost:3010 | admin@sqlpad.local / (see `.env`) | SQL query tool |

---

## Infrastructure Layer

### 1. PostgreSQL (Consolidated)

**Image:** `postgres:18.1`
**Container:** `chat-postgres`
**Port:** 5432 (localhost only)

**Purpose:** Single PostgreSQL instance hosting 3 logical databases

**Databases:**

| Database | User | Purpose | Connection String |
|----------|------|---------|-------------------|
| `main_db` | `main_user` | Backend/Engine data | `postgresql://main_user:***@postgres:5432/main_db` |
| `langfuse` | `langfuse` | Langfuse observability | `postgresql://langfuse:***@postgres:5432/langfuse` |
| `litellm` | `litellm` | LiteLLM metadata | `postgresql://litellm:***@postgres:5432/litellm` |

**Initialization:**
- Databases created via `/docker-entrypoint-initdb.d/` scripts
- Script: `scripts/postgres-init/01-create-databases.sh`
- Runs only on first startup (empty volume)

**Volume:** `postgres_data:/var/lib/postgresql`

---

### 2. Redis Stack (Consolidated)

**Image:** `redis/redis-stack-server:latest`
**Container:** `chat-redis-stack`
**Port:** 6379 (localhost only)

**Purpose:** Single Redis instance with vector search, cache, pub/sub capabilities

**Database Allocation:**

| DB # | Service | Purpose | Connection String |
|------|---------|---------|-------------------|
| 0 | Main Application | Cache, vectors, pub/sub | `redis://redis-stack:6379/0` |
| 1 | Langfuse | Queue, cache | `redis://redis-stack:6379/1` |
| 2 | LiteLLM | Response cache, dedup | `redis://redis-stack:6379/2` |
| 3-15 | Reserved | Future services | - |

**Configuration:**
- Max Memory: 1024MB
- Eviction Policy: `noeviction` (critical for Langfuse)
- Persistence: AOF enabled
- Protected Mode: Disabled (Docker network only)

**Volume:** `redis_data:/data`

---

### 3. MSSQL Server

**Image:** `mcr.microsoft.com/mssql/server:2025-latest`
**Container:** `chat-mssql`
**Port:** 1433 (localhost only)

**Purpose:** Microsoft SQL Server for enterprise data warehouse

**Credentials:**
- User: `sa`
- Password: (see `.env`)

**Volumes:**
- Data: `mssql_data:/var/opt/mssql/data`
- Logs: `mssql_logs:/var/opt/mssql/log`

---

## Supporting Services

### 4. ClickHouse

**Image:** `clickhouse/clickhouse-server:latest`
**Container:** `chat-clickhouse`
**Ports:** 8123 (HTTP), 9000 (Native) - localhost only

**Purpose:** Analytics database for Langfuse v3 (traces, spans, events)

**Configuration:**
- Database: `langfuse`
- User: `langfuse`
- Password: See `.env`

**Volumes:**
- Data: `clickhouse_data:/var/lib/clickhouse`
- Logs: `clickhouse_logs:/var/log/clickhouse-server`

---

### 5. MinIO

**Image:** `minio/minio:latest`
**Container:** `chat-minio`
**Ports:**
- API: 9090 (public)
- Console: 9091 (public)

**Purpose:** S3-compatible object storage for Langfuse (file uploads, events, exports)

**Buckets:**
- `langfuse` - Auto-created on startup

**Credentials:**
- Root User: `minioadmin`
- Root Password: (see `.env`)

**Access:**
- Console: http://localhost:9091
- API: http://localhost:9090

**Volume:** `minio_data:/data`

---

### 6. SQLPad

**Image:** `sqlpad/sqlpad:latest` (custom build with ODBC)
**Container:** `chat-sqlpad`
**Port:** 3010 (localhost only)

**Purpose:** Web-based SQL editor for database exploration

**Credentials:**
- Admin: `admin@sqlpad.local`
- Password: (see `.env`)

**Pre-configured Connections:**
- MSSQL Server (localhost:1433)

**Volume:** `sqlpad_data:/var/lib/sqlpad`

---

## Observability & Gateway

### 7. Langfuse Web (v3)

**Image:** `langfuse/langfuse:3`
**Container:** `chat-langfuse-web`
**Port:** 3000 (public)

**Purpose:** LLM observability platform for tracing, monitoring, and debugging

**Key Features:**
- Trace ingestion and visualization
- Span and generation tracking
- Cost tracking and analytics
- User feedback collection
- Prompt management

**Configuration:**
- Database: PostgreSQL `langfuse` database
- Cache: Redis DB 1
- Analytics: ClickHouse
- Storage: MinIO

**Initialization:**
- Organization: `Zuna Organization`
- Project: `Zuna Project`
- User: `admin@example.com` / (see `.env`)

**API Keys:**
- Public Key: `lf_pk_a7b3c9d2e8f4a1b6c5d9e2f7a3b8c4d1`
- Secret Key: `lf_sk_f2a8b7c3d9e1f6a4b2c7d8e3f9a1b5c6d2e8f4a9b3c1d7e2f8a4b6c9d1e5f3a7`

**Health Check:** http://localhost:3000/api/public/health

---

### 8. Langfuse Worker (v3)

**Image:** `langfuse/langfuse-worker:3`
**Container:** `chat-langfuse-worker`
**Port:** 3030 (localhost only)

**Purpose:** Background job processor for Langfuse (exports, aggregations, cleanup)

**Configuration:**
- Shares same database, cache, and storage as Langfuse Web
- Processes async jobs from Redis queue

---

### 9. LiteLLM Proxy

**Image:** `ghcr.io/berriai/litellm:main-stable`
**Container:** `chat-litellm`
**Port:** 4000 (public)

**Purpose:** Unified LLM gateway for OpenAI-compatible API access

**Supported Models:**
- `gpt-4.1` - Azure OpenAI GPT-4
- `text-embedding-3-small` - Azure OpenAI Embeddings
- `cohere-rerank-v3.5` - Azure AI Cohere Rerank

**Configuration:**
- Config File: `configs/litellm/config.yaml`
- Database: PostgreSQL `litellm` database
- Cache: Redis DB 2
- Observability: Langfuse integration

**Authentication:**
- Master Key: `sk-1234567890abcdef` (see `.env`)
- UI Credentials: `admin` / (see `.env`)

**Endpoints:**
- Health: http://localhost:4000/health/liveliness
- API: http://localhost:4000/v1/*
- UI: http://localhost:4000/ui

**Features:**
- Request caching (Redis)
- Load balancing
- Cost tracking
- Langfuse tracing integration

---

## Application Layer

### 10. Frontend (React + Vite)

**Container:** `chat-frontend`
**Port:** 5173 (public)

**Purpose:** React-based user interface

**Technology Stack:**
- React 18
- Vite (dev server with HMR)
- TypeScript
- Material-UI / Tailwind

**Configuration:**
- Backend URL: http://localhost:8000
- Mode: Local (hot reload enabled)

**Build:**
- Dev: `npm run dev`
- Production: `npm run build`

---

### 11. Backend (FastAPI)

**Container:** `chat-backend`
**Port:** 8000 (public)

**Purpose:** Main application API server

**Technology Stack:**
- Python 3.12
- FastAPI
- Pydantic Settings
- Loguru logging

**Configuration:**
- Settings: `configs/settings.py` (Pydantic)
- Config Wrapper: `backend/app/config.py`
- Logs: `logs/backend/`

**Health Endpoint:** http://localhost:8000/health

**API Documentation:** http://localhost:8000/docs

**Dependencies:**
- Engine: http://engine:8001
- PostgreSQL: main_db
- Redis: DB 0
- LiteLLM: http://litellm:4000
- Langfuse: http://langfuse-web:3000

---

### 12. Engine (FastAPI)

**Container:** `chat-engine`
**Port:** 8001 (internal only)

**Purpose:** Message processing engine

**Technology Stack:**
- Python 3.12
- FastAPI
- Pydantic Settings
- Loguru logging

**Configuration:**
- Settings: `configs/settings.py` (Pydantic)
- Config Wrapper: `engine/app/config.py`
- Logs: `logs/engine/`

**Security:**
- CORS: Restricted to backend only
- Not directly accessible from frontend

**Health Endpoint:** http://localhost:8001/health (internal)

**Dependencies:**
- PostgreSQL: main_db
- Redis: DB 0
- LiteLLM: http://litellm:4000
- Langfuse: http://langfuse-web:3000

---

## Service Dependencies

### Startup Order (4 Layers)

**Layer 1: Infrastructure** (No dependencies)
```
postgres → redis-stack → mssql
```

**Layer 2: Data & Analytics** (Depends on Layer 1)
```
clickhouse → minio → minio-init (bucket creation)
```

**Layer 3: Observability & Gateway** (Depends on Layer 1 & 2)
```
langfuse-web (requires: postgres, redis, clickhouse, minio)
langfuse-worker (requires: postgres, redis, clickhouse, minio)
litellm (requires: postgres, redis)
```

**Layer 4: Application** (Depends on Layer 1 & 3)
```
engine (requires: postgres, redis, langfuse-web, litellm)
backend (requires: postgres, redis, engine, langfuse-web, litellm)
frontend (requires: backend)
```

**Layer 5: Support Tools** (Depends on specific services)
```
sqlpad (requires: mssql)
```

---

## Resource Usage

### Consolidated vs Separate

**Before Consolidation:**
- 6 database containers (3 PostgreSQL + 3 Redis)
- 11 Docker volumes
- ~8GB RAM usage

**After Consolidation:**
- 2 database containers (1 PostgreSQL + 1 Redis)
- 8 Docker volumes
- ~6GB RAM usage
- **Savings:** 4 fewer containers, ~2GB RAM

### Volume List

```
z_postgres_data       PostgreSQL data
z_redis_data          Redis data
z_mssql_data          MSSQL data
z_mssql_logs          MSSQL logs
z_clickhouse_data     ClickHouse data
z_clickhouse_logs     ClickHouse logs
z_minio_data          MinIO data
z_sqlpad_data         SQLPad data
```

---

## Network Configuration

All services are in the `chat_network` bridge network, enabling service-to-service communication via container names.

### Port Exposure Strategy

**Public Ports** (0.0.0.0):
- 5173 - Frontend
- 8000 - Backend API
- 3000 - Langfuse Web
- 4000 - LiteLLM
- 9090, 9091 - MinIO

**Localhost Only** (127.0.0.1):
- 5432 - PostgreSQL
- 6379 - Redis
- 1433 - MSSQL
- 8123, 9000 - ClickHouse
- 3010 - SQLPad
- 3030 - Langfuse Worker

**Internal Only** (No host binding):
- 8001 - Engine (via backend only)

---

## Configuration Management

All services are configured via:

1. **Environment Variables** - `.env` file (not committed to git)
2. **Pydantic Settings** - `configs/settings.py` (centralized type-safe configuration)
3. **Docker Compose** - `docker-compose.yml` (service orchestration)
4. **Init Scripts** - `scripts/` (database initialization)
5. **Config Files** - `configs/` (service-specific YAML configs)

### Settings Architecture

```
.env (source of truth)
  ↓
configs/settings.py (Pydantic Settings)
  ↓
├─ backend/app/config.py (Backend wrapper)
└─ engine/app/config.py (Engine wrapper)
```

All infrastructure settings (PostgreSQL, Redis, Langfuse, LiteLLM, Azure) are accessible via:

```python
from app.config import settings

settings.postgres.main_database_url
settings.redis.main_redis_url
settings.langfuse.langfuse_host
settings.litellm.litellm_base_url
settings.azure_openai.azure_openai_endpoint
```

---

## Monitoring & Observability

### Health Checks

All services implement health checks:

```bash
# Backend
curl http://localhost:8000/health

# Engine
curl http://localhost:8001/health

# Langfuse
curl http://localhost:3000/api/public/health

# LiteLLM
curl http://localhost:4000/health/liveliness

# Docker health status
docker ps --filter "name=chat-" --format "table {{.Names}}\t{{.Status}}"
```

### Logs

**Docker Logs:**
```bash
docker logs chat-backend
docker logs chat-engine
docker logs chat-langfuse-web
docker logs chat-litellm
```

**File Logs:**
- Backend: `logs/backend/`
- Engine: `logs/engine/`
- Loguru format: JSON + colorized console

### Tracing

LLM calls can be traced via Langfuse:
- Automatic: LiteLLM → Langfuse integration
- Manual: Use Langfuse SDK in backend/engine

---

## Security Considerations

### Production Checklist

- [ ] Change all passwords in `.env`
- [ ] Generate new encryption keys for Langfuse
- [ ] Use secrets management (Vault, AWS Secrets Manager)
- [ ] Enable TLS/SSL for database connections
- [ ] Configure firewall rules
- [ ] Use separate Redis instances (not DB numbers)
- [ ] Use separate PostgreSQL instances
- [ ] Enable Redis authentication
- [ ] Review CORS settings
- [ ] Remove localhost bindings for production
- [ ] Use reverse proxy (nginx/traefik) for HTTPS
- [ ] Implement rate limiting
- [ ] Enable audit logging
- [ ] Set up monitoring and alerting

---

## Backup & Disaster Recovery

### Database Backups

**PostgreSQL:**
```bash
# Backup all databases
docker exec chat-postgres pg_dumpall -U postgres > backup.sql

# Backup specific database
docker exec chat-postgres pg_dump -U main_user main_db > main_db_backup.sql
```

**Redis:**
```bash
# Trigger save
docker exec chat-redis-stack redis-cli SAVE

# Copy RDB file
docker cp chat-redis-stack:/data/dump.rdb ./redis_backup.rdb
```

**ClickHouse:**
```bash
docker exec chat-clickhouse clickhouse-client --query "BACKUP DATABASE langfuse"
```

### Volume Backups

```bash
# Stop services
docker-compose down

# Backup volumes
docker run --rm -v z_postgres_data:/data -v $(pwd):/backup ubuntu tar czf /backup/postgres_backup.tar.gz /data

# Restore volumes
docker run --rm -v z_postgres_data:/data -v $(pwd):/backup ubuntu tar xzf /backup/postgres_backup.tar.gz -C /
```

---

## Next Steps

1. **Integration Testing** - Run `./tests/integration/test_*.sh`
2. **Configure LLM Models** - Update `configs/litellm/config.yaml`
3. **Enable Langfuse Tracing** - Add Langfuse SDK to backend/engine
4. **Production Deployment** - Follow security checklist
5. **Monitoring Setup** - Configure Prometheus/Grafana

---

**Last Updated:** 2025-12-31
**Version:** 1.0.0
**Author:** Infrastructure Consolidation Project
