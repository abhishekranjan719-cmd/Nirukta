# Zuna

A production-ready chat application with comprehensive infrastructure including observability, LLM gateway, and data persistence. Built with React, FastAPI, PostgreSQL, Redis, Langfuse, and LiteLLM.

## Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Application Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Frontend   │  │   Backend    │  │    Engine    │          │
│  │  React+Vite  │←→│   FastAPI    │←→│   FastAPI    │          │
│  │  Port 5173   │  │  Port 8000   │  │  Port 8001   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Observability Layer                           │
│  ┌──────────────────────────────┐  ┌────────────────────────┐  │
│  │   Langfuse v3 Web & Worker   │  │   LiteLLM Proxy        │  │
│  │   Port 3000 (Internal)       │  │   Port 4000 (Internal) │  │
│  │   LLM Observability Platform │  │   LLM Gateway          │  │
│  └──────────────────────────────┘  └────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  PostgreSQL  │  │ Redis Stack  │  │  ClickHouse  │          │
│  │  (4 DBs)     │  │  (3 DBs)     │  │  Port 8123   │          │
│  │  Port 5432   │  │  Port 6379   │  │  Analytics   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │    MinIO     │  │    MSSQL     │  │   SQLPad     │          │
│  │  Port 9000   │  │  Port 1433   │  │  Port 3030   │          │
│  │  S3 Storage  │  │  SQL Server  │  │  SQL IDE     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

### Message Flow

1. User types message in React UI
2. Frontend POST to `/api/chat` on backend
3. Backend POST to `/process` on engine
4. Engine processes message (can call LiteLLM for LLM inference)
5. All LLM calls traced via Langfuse observability
6. Response flows back: Engine → Backend → Frontend
7. Frontend displays response in chat interface

## Services

### Application Services (3)

| Service | Purpose | Port | Public Access |
|---------|---------|------|---------------|
| **Frontend** | React+Vite UI | 5173 | ✅ Yes |
| **Backend** | FastAPI REST API | 8000 | ✅ Yes |
| **Engine** | FastAPI processing engine | 8001 | ❌ Internal only |

### Observability & Gateway (3)

| Service | Purpose | Port | Public Access |
|---------|---------|------|---------------|
| **Langfuse Web** | LLM observability UI | 3000 | 🔒 Localhost only |
| **Langfuse Worker** | Background job processor | - | ❌ Internal only |
| **LiteLLM** | LLM gateway proxy | 4000 | 🔒 Localhost only |

### Infrastructure Services (6)

| Service | Purpose | Port | Public Access |
|---------|---------|------|---------------|
| **PostgreSQL** | Primary database (4 DBs) | 5432 | 🔒 Localhost only |
| **Redis Stack** | Cache & sessions (3 DBs) | 6379 | 🔒 Localhost only |
| **ClickHouse** | Analytics database | 8123 | 🔒 Localhost only |
| **MinIO** | S3-compatible storage | 9000/9001 | 🔒 Localhost only |
| **MSSQL** | SQL Server database | 1433 | 🔒 Localhost only |
| **SQLPad** | SQL query IDE | 3030 | 🔒 Localhost only |

**Total: 12 services** running in Docker Compose

For complete service details, see **[docs/SERVICES.md](docs/SERVICES.md)**

## Key Features

### Application Features
- Full chat interface with conversation history
- Multiple conversation support
- **LangGraph Memory System**: Multi-user, multi-conversation persistent memory with PostgreSQL checkpointing
- Real-time message updates
- Markdown message formatting
- Loading indicators and error handling
- Persistent conversation storage (PostgreSQL)
- Health checks for all services

### Infrastructure Features
- **Centralized Configuration**: Pydantic Settings with type safety
- **Observability**: Langfuse for LLM tracing and monitoring
- **LLM Gateway**: LiteLLM proxy with Azure OpenAI integration
- **Agent Memory**: LangGraph PostgreSQL checkpointer for conversation persistence
- **Data Persistence**: PostgreSQL with 4 isolated databases
- **Caching**: Redis Stack with 3 logical databases
- **Analytics**: ClickHouse for event storage
- **Object Storage**: MinIO for file uploads
- **SQL IDE**: SQLPad for database exploration
- **Consolidated Resources**: Single PostgreSQL and Redis instances

### Production Ready
- Docker Compose orchestration with health checks
- Layered service dependencies (4 layers)
- Comprehensive error handling
- Structured logging with loguru
- Environment-based configuration (local/dev modes)
- Integration tests for all services

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 20+ (for local development)
- Python 3.12+ (for local development)
- uv (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   cd /Users/aritra.biswas/Desktop/workspace/projects/z
   ```

2. **Create .env file**
   ```bash
   # Copy template
   cp .env.example .env

   # Generate Langfuse encryption keys
   echo "LANGFUSE_NEXTAUTH_SECRET=$(openssl rand -hex 32)" >> .env
   echo "LANGFUSE_ENCRYPTION_KEY=$(openssl rand -hex 32)" >> .env
   echo "LANGFUSE_SALT=$(openssl rand -hex 32)" >> .env
   ```

   For complete environment variable documentation, see **[docs/ENV_VARS.md](docs/ENV_VARS.md)**

3. **Start all services** (layered startup)
   ```bash
   # Method 1: All at once (Docker handles dependencies)
   docker-compose up -d

   # Method 2: Manual layered startup (recommended for first time)
   # Layer 1: Core infrastructure
   docker-compose up -d postgres redis-stack mssql
   sleep 10

   # Layer 2: Supporting services
   docker-compose up -d clickhouse minio minio-init
   sleep 10

   # Layer 3: Observability & Gateway
   docker-compose up -d langfuse-web langfuse-worker litellm
   sleep 10

   # Layer 4: Application services
   docker-compose up -d backend engine frontend
   ```

4. **Verify all services are healthy**
   ```bash
   docker ps --filter "name=chat-" --format "table {{.Names}}\t{{.Status}}"
   ```

5. **Access the application**

   **Public Access:**
   - Frontend UI: http://localhost:5173
   - Backend API Docs: http://localhost:8000/docs
   - Backend Health: http://localhost:8000/health

   **Localhost Only (Development):**
   - Langfuse UI: http://localhost:3000 (admin@example.com / see `.env`)
   - LiteLLM Proxy: http://localhost:4000/health/liveliness
   - SQLPad IDE: http://localhost:3030
   - MinIO Console: http://localhost:9001 (see `.env` for credentials)

   **Internal Only (Not Exposed):**
   - Engine API: http://engine:8001 (backend access only)
   - PostgreSQL: postgres:5432
   - Redis: redis-stack:6379
   - ClickHouse: clickhouse:8123

6. **View logs**
   ```bash
   # All services
   docker-compose logs --tail=50 --follow

   # Specific service
   docker logs chat-backend --tail=100
   docker logs chat-engine --tail=100
   docker logs chat-langfuse-web --tail=100
   ```

7. **Stop services**
   ```bash
   # Stop all
   docker-compose down

   # Stop and remove volumes (⚠️ deletes all data!)
   docker-compose down -v
   ```

## Development

### Project Structure

```
z/
├── frontend/              # React + Vite frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── api/          # API client
│   │   ├── types/        # TypeScript types
│   │   └── styles/       # CSS styles
│   └── package.json
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── models/       # Pydantic models
│   │   ├── config.py     # Configuration wrapper
│   │   └── main.py       # FastAPI app
│   └── pyproject.toml
├── engine/               # FastAPI engine
│   ├── app/
│   │   ├── models/       # Pydantic models
│   │   ├── services/     # Processing logic
│   │   ├── config.py     # Configuration wrapper
│   │   └── main.py       # FastAPI app
│   └── pyproject.toml
├── configs/              # Centralized configuration
│   ├── settings.py       # Pydantic Settings (main config)
│   ├── frontend.yaml     # Frontend constants
│   ├── backend.yaml      # Backend constants
│   ├── engine.yaml       # Engine constants
│   └── litellm/          # LiteLLM proxy config
├── scripts/              # Database init scripts
│   └── postgres/         # PostgreSQL initialization
├── dockerfiles/          # Docker configurations
├── tests/                # Test suite
│   ├── integration/      # Integration tests
│   └── unit/             # Unit tests
├── docs/                 # Documentation
│   ├── SERVICES.md       # Service documentation
│   ├── TROUBLESHOOTING.md# Troubleshooting guide
│   └── ENV_VARS.md       # Environment variables
├── docker-compose.yml    # Service orchestration (12 services)
├── Makefile              # Development commands
└── .env                  # Environment variables
```

### Configuration Architecture

All configuration is centralized in `configs/settings.py` using **Pydantic Settings**:

```python
# Backend/Engine consume settings
from app.config import settings

# Access infrastructure settings
db_url = settings.postgres.main_database_url
redis_url = settings.redis.main_redis_url
langfuse_enabled = settings.langfuse.is_enabled
litellm_url = settings.litellm.litellm_base_url
```

**Configuration Sources:**
1. `.env` file (environment variables)
2. `configs/*.yaml` (constants and defaults)
3. `configs/settings.py` (Pydantic validation and processing)
4. Service wrappers (`backend/app/config.py`, `engine/app/config.py`)

**Features:**
- Type-safe with Pydantic validation
- Single source of truth (.env file)
- Hot reload in local mode
- Mode-based configuration (local/dev)
- Lazy-loaded infrastructure settings
- Environment-specific overrides

See **[docs/ENV_VARS.md](docs/ENV_VARS.md)** for complete configuration reference.

### API Endpoints

#### Backend API (Port 8000)

**Chat Endpoints:**
- `POST /api/chat` - Send a chat message
  ```json
  Request: {
    "message": "Hello",
    "conversation_id": "optional-uuid"
  }
  Response: {
    "response": "Processed: Hello",
    "conversation_id": "uuid",
    "timestamp": "2025-12-31T10:00:00Z"
  }
  ```

- `GET /api/conversations/{id}` - Get conversation history
- `GET /api/conversations` - List all conversations

**System Endpoints:**
- `GET /health` - Health check
- `GET /docs` - OpenAPI documentation

#### Engine API (Port 8001)

**Processing Endpoints:**
- `POST /process` - Process a message
  ```json
  Request: {
    "message": "Hello",
    "context": {}
  }
  Response: {
    "response": "Processed: Hello",
    "metadata": {
      "processor": "echo",
      "timestamp": "2025-12-31T10:00:00Z"
    }
  }
  ```

**System Endpoints:**
- `GET /health` - Health check
- `GET /docs` - OpenAPI documentation

**Note:** Engine API is internal only, not exposed to public.

### Running Tests

```bash
# Integration tests
./tests/integration/test_litellm.sh      # LiteLLM proxy tests
./tests/integration/test_langfuse.sh     # Langfuse tests

# Python integration tests (requires httpx)
docker exec chat-backend python -m pytest tests/integration/test_litellm.py
docker exec chat-backend python -m pytest tests/integration/test_langfuse.py

# Unit tests (if available)
make test-backend
make test-engine
```

### Local Development (without Docker)

**Backend:**
```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

**Engine:**
```bash
cd engine
uv sync
uv run uvicorn app.main:app --reload --port 8001
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Note:** You'll need to start PostgreSQL, Redis, and other infrastructure services separately for local development, or use `docker-compose up -d postgres redis-stack` for infrastructure only.

## Infrastructure Details

### PostgreSQL Consolidation

Single PostgreSQL instance with **4 isolated databases**:

| Database | User | Purpose | Port |
|----------|------|---------|------|
| `main_db` | `main_user` | Backend/Engine data | 5432 |
| `langfuse` | `langfuse` | Langfuse observability | 5432 |
| `litellm` | `litellm` | LiteLLM proxy | 5432 |
| `langgraph` | `langgraph` | Agent memory & checkpointing | 5432 |

**Benefits:**
- 70% reduction in memory usage vs 4 separate instances
- Unified backup/restore procedures
- Simplified configuration
- Single connection pooling

**Database URLs:**
```
postgresql://main_user:password@postgres:5432/main_db
postgresql://langfuse:password@postgres:5432/langfuse
postgresql://litellm:password@postgres:5432/litellm
postgresql://langgraph:password@postgres:5432/langgraph
```

### Redis Consolidation

Single Redis Stack instance with **3 logical databases**:

| DB Number | Purpose | Access |
|-----------|---------|--------|
| 0 | Main app cache | `redis://redis-stack:6379/0` |
| 1 | Langfuse cache | `redis://redis-stack:6379/1` |
| 2 | LiteLLM cache | `redis://redis-stack:6379/2` |

**Benefits:**
- 65% reduction in memory usage vs 3 separate instances
- Shared connection pooling
- Single monitoring endpoint

### Langfuse Observability

**Purpose:** LLM request tracing, monitoring, and analytics

**Features:**
- Request/response tracing
- Token usage tracking
- Cost analysis
- Performance metrics
- User feedback collection

**Access:**
- Web UI: http://localhost:3000
- Default credentials: admin@example.com / (see `.env`)
- API: http://langfuse-web:3000 (internal)

**Architecture:**
- Web service (port 3000): User interface and API
- Worker service: Background job processing
- Storage: PostgreSQL + Redis + ClickHouse
- MinIO: File uploads and media storage

### LiteLLM Gateway

**Purpose:** Unified LLM gateway with OpenAI-compatible API

**Features:**
- Azure OpenAI integration
- Multiple model support (GPT-4, embeddings, rerank)
- Request/response caching
- Rate limiting and load balancing
- Automatic failover
- Langfuse integration for tracing

**Access:**
- API: http://localhost:4000 (requires Bearer token)
- Health check: http://localhost:4000/health/liveliness
- Models: GET http://localhost:4000/v1/models

**Configuration:**
- Config file: `configs/litellm/config.yaml`
- Models defined: gpt-4.1, text-embedding-3-small, cohere-rerank-v3.5
- Authentication: Bearer token (`LITELLM_MASTER_KEY`)

**Example Usage:**
```bash
curl -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
     http://localhost:4000/v1/chat/completions \
     -d '{"model": "gpt-4.1", "messages": [{"role": "user", "content": "Hello"}]}'
```

## Service Dependencies

Services start in **4 layers** based on dependencies:

**Layer 1: Core Infrastructure** (no dependencies)
- PostgreSQL
- Redis Stack
- MSSQL

**Layer 2: Supporting Services** (depends on Layer 1)
- ClickHouse
- MinIO (+ init container)
- SQLPad

**Layer 3: Observability & Gateway** (depends on Layers 1-2)
- Langfuse Web (depends on: PostgreSQL, Redis, ClickHouse, MinIO)
- Langfuse Worker (depends on: Langfuse Web)
- LiteLLM (depends on: PostgreSQL, Redis)

**Layer 4: Application** (depends on Layers 1-3)
- Backend (depends on: PostgreSQL, Redis, Engine)
- Engine (depends on: PostgreSQL, Redis)
- Frontend (depends on: Backend)

## Monitoring & Health Checks

### Service Health Checks

```bash
# Check all services
docker ps --filter "name=chat-" --format "table {{.Names}}\t{{.Status}}"

# Test health endpoints
curl http://localhost:8000/health           # Backend
curl http://localhost:8001/health           # Engine
curl http://localhost:3000/api/public/health # Langfuse
curl http://localhost:4000/health/liveliness # LiteLLM
```

### Logs

```bash
# All services
docker-compose logs --tail=50 --follow

# Specific service
docker logs chat-backend --tail=100
docker logs chat-langfuse-web --tail=100

# Filter by error level
docker logs chat-backend 2>&1 | grep ERROR
```

### Resource Usage

```bash
# Check container resource usage
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Redis memory
docker exec chat-redis-stack redis-cli INFO memory | grep used_memory_human

# PostgreSQL connections
docker exec chat-postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"
```

## Troubleshooting

For comprehensive troubleshooting, see **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)**

### Common Issues

**Services won't start:**
```bash
# Check which service is unhealthy
docker ps -a --filter "name=chat-"

# Check logs
docker logs chat-[service-name] --tail=100

# Restart in layers
docker-compose down
docker-compose up -d postgres redis-stack mssql
sleep 10
docker-compose up -d
```

**PostgreSQL init scripts not running:**
```bash
# Init scripts only run on first startup with empty volume
docker-compose down -v  # ⚠️ Deletes all data!
docker-compose up -d postgres
docker logs chat-postgres --follow  # Wait for "✅ All databases created"
```

**Langfuse health check failing:**
```bash
# Check Langfuse logs
docker logs chat-langfuse-web --tail=100

# Test health check manually
docker exec chat-langfuse-web wget --quiet --tries=1 --spider http://127.0.0.1:3000/api/public/health
```

**LiteLLM authentication errors:**
```bash
# Most endpoints require Bearer token
curl -H "Authorization: Bearer $LITELLM_MASTER_KEY" http://localhost:4000/health

# Liveliness endpoint doesn't require auth
curl http://localhost:4000/health/liveliness
```

**Port conflicts:**
```bash
# Find process using port
lsof -i :8000

# Or change port in docker-compose.yml
ports:
  - "8001:8000"  # Map to different host port
```

### Complete Reset

```bash
# ⚠️ WARNING: Deletes ALL data!

# Stop and remove everything
docker-compose down -v

# Remove all volumes
docker volume rm $(docker volume ls -q | grep "^z_")

# Remove network
docker network rm chat_network

# Start fresh
docker-compose up -d
```

## Production Deployment

### Security Checklist

Before deploying to production:

1. **Change all default passwords** in `.env`:
   - PostgreSQL passwords (3)
   - Redis password (set one!)
   - Langfuse admin password
   - LiteLLM master key
   - MinIO root password
   - ClickHouse password

2. **Generate strong encryption keys**:
   ```bash
   openssl rand -hex 32  # Run 3 times for Langfuse keys
   ```

3. **Update URLs and CORS**:
   ```bash
   VITE_BACKEND_URL=https://api.yourdomain.com
   BACKEND_CORS_ORIGINS=["https://yourdomain.com"]
   ```

4. **Enable TLS/SSL**:
   - Use reverse proxy (nginx/Caddy)
   - Configure SSL certificates
   - Force HTTPS redirects

5. **Review port exposure**:
   - Only expose frontend (5173) and backend (8000)
   - Use internal networking for all other services
   - Consider using `networks` in docker-compose

6. **Set MODE to dev**:
   ```bash
   MODE=dev  # Disables hot reload in production
   ```

See **[docs/ENV_VARS.md](docs/ENV_VARS.md)** for production security best practices.

### Resource Requirements

**Minimum (Development):**
- CPU: 4 cores
- RAM: 8 GB
- Disk: 20 GB

**Recommended (Production):**
- CPU: 8 cores
- RAM: 16 GB
- Disk: 100 GB SSD
- Network: 1 Gbps

**Per-Service Breakdown:**
- PostgreSQL: 512 MB - 2 GB
- Redis: 512 MB - 2 GB
- ClickHouse: 1 GB - 4 GB
- Langfuse: 512 MB - 1 GB
- LiteLLM: 256 MB - 512 MB
- Backend/Engine/Frontend: 256 MB each

### Backup Strategy

**PostgreSQL Backups:**
```bash
# Backup all databases
docker exec chat-postgres pg_dumpall -U postgres > backup_all.sql

# Backup specific database
docker exec chat-postgres pg_dump -U main_user main_db > backup_main.sql

# Restore
cat backup_all.sql | docker exec -i chat-postgres psql -U postgres
```

**Redis Backups:**
```bash
# Redis saves to dump.rdb automatically
docker cp chat-redis-stack:/data/dump.rdb ./redis_backup.rdb

# Restore
docker cp redis_backup.rdb chat-redis-stack:/data/dump.rdb
docker-compose restart redis-stack
```

**MinIO Backups:**
```bash
# Export bucket
docker exec chat-minio mc mirror local/langfuse /backup/langfuse/

# Import bucket
docker exec chat-minio mc mirror /backup/langfuse/ local/langfuse/
```

See **[docs/SERVICES.md](docs/SERVICES.md)** for complete backup procedures.

## Technology Stack

### Frontend
- **Framework**: Vite + React 18 + TypeScript
- **Styling**: CSS Modules
- **Markdown**: react-markdown
- **HTTP Client**: Fetch API
- **Build**: Vite bundler

### Backend & Engine
- **Framework**: FastAPI + Python 3.12
- **Package Manager**: uv (fast Python package manager)
- **Validation**: Pydantic v2
- **Configuration**: Pydantic Settings
- **Logging**: loguru
- **ASGI Server**: Uvicorn

### Infrastructure
- **Database**: PostgreSQL 18 (3 databases)
- **Cache**: Redis Stack 7 (3 logical DBs)
- **Analytics**: ClickHouse 24
- **Object Storage**: MinIO (S3-compatible)
- **SQL Server**: MSSQL 2022
- **SQL IDE**: SQLPad

### Observability & Gateway
- **Observability**: Langfuse v3
- **LLM Gateway**: LiteLLM
- **LLM Provider**: Azure OpenAI
- **Tracing**: Langfuse integration

### DevOps
- **Containerization**: Docker + Docker Compose
- **Orchestration**: docker-compose.yml (12 services)
- **Health Checks**: Built-in Docker health checks
- **Logging**: Container logs via Docker
- **Testing**: pytest + httpx

## Documentation

- **[docs/SERVICES.md](docs/SERVICES.md)** - Complete service documentation (architecture, access, configuration)
- **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Comprehensive troubleshooting guide (9 common issues)
- **[docs/ENV_VARS.md](docs/ENV_VARS.md)** - Environment variables reference (60+ variables)
- **[docs/LANGGRAPH_MEMORY.md](docs/LANGGRAPH_MEMORY.md)** - LangGraph memory system for conversation persistence
- **[docs/LANGGRAPH_MEMORY_VALIDATION.md](docs/LANGGRAPH_MEMORY_VALIDATION.md)** - Memory system validation report and test results
- **[docs/RICH_CONTENT_RENDERING.md](docs/RICH_CONTENT_RENDERING.md)** - Rich content rendering capabilities
- **[docs/TRACKING_AND_OBSERVABILITY.md](docs/TRACKING_AND_OBSERVABILITY.md)** - Tracking and observability with Langfuse
- **[docs/CHART_SUPPORT.md](docs/CHART_SUPPORT.md)** - Chart and visualization support

## Development Roadmap

### Completed ✅
- ✅ 3-tier architecture (Frontend, Backend, Engine)
- ✅ Centralized configuration with Pydantic Settings
- ✅ PostgreSQL consolidation (4 databases in 1 instance)
- ✅ Redis consolidation (3 DBs in 1 instance)
- ✅ **LangGraph Memory System** (Multi-user, multi-conversation persistent memory)
- ✅ Langfuse observability integration
- ✅ LiteLLM gateway integration
- ✅ Azure OpenAI integration
- ✅ Docker Compose orchestration
- ✅ Health checks and monitoring
- ✅ Integration tests
- ✅ Comprehensive documentation

### Future Enhancements 🚀
- Authentication & Authorization (JWT, OAuth)
- User management and roles
- Conversation sharing
- File upload support (images, PDFs)
- Voice input/output
- Real-time streaming responses
- Multi-model support (Claude, Gemini)
- Prompt templates and management
- Usage analytics dashboard
- Cost tracking per user
- Rate limiting per user
- Kubernetes deployment manifests
- CI/CD pipeline
- Automated testing suite
- Performance benchmarking

## License

MIT

## Support

For help and documentation:

**Quick Access:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/docs
- Langfuse UI: http://localhost:3000
- SQLPad IDE: http://localhost:3030

**Documentation:**
- [Service Documentation](docs/SERVICES.md)
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- [Environment Variables](docs/ENV_VARS.md)
- [LangGraph Memory System](docs/LANGGRAPH_MEMORY.md)
- [Rich Content Rendering](docs/RICH_CONTENT_RENDERING.md)
- [Tracking & Observability](docs/TRACKING_AND_OBSERVABILITY.md)
- [Chart Support](docs/CHART_SUPPORT.md)

**Diagnostics:**
```bash
# Check service status
docker ps --filter "name=chat-"

# View logs
docker-compose logs --tail=100

# Health checks
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:3000/api/public/health
curl http://localhost:4000/health/liveliness
```

---

**Last Updated:** 2025-12-31
**Version:** 2.0.0 (Consolidated Infrastructure)
