# Infrastructure Consolidation Plan

## Executive Summary
Consolidate multiple PostgreSQL and Redis instances into single shared instances while maintaining logical separation through databases and Redis DB numbers. This reduces resource overhead while preserving isolation for development environments.

---

## Current State Analysis (from docker-compose.backup)

### Current PostgreSQL Instances (3 separate)
1. **postgres:18.1-alpine** - Main application database (port 5432)
2. **langfuse_db** (postgres:18.1-alpine) - Langfuse database
3. **litellm_db** (postgres:18.1-alpine) - LiteLLM database

### Current Redis Instances (3 separate)
1. **redis_stack** - Main Redis Stack (port 6379)
2. **langfuse_redis** - Langfuse cache/queue (port 6380)
3. **litellm_redis** - LiteLLM cache (port 6381)

### Other Required Services
- **MSSQL**: mcr.microsoft.com/mssql/server:2025-latest
- **ClickHouse**: clickhouse/clickhouse-server:latest (Langfuse v3 requirement)
- **MinIO**: minio/minio:latest (S3-compatible storage for Langfuse v3)
- **SQLPad**: Custom build with ODBC support
- **Langfuse Web**: langfuse/langfuse:3
- **Langfuse Worker**: langfuse/langfuse-worker:3
- **LiteLLM**: ghcr.io/berriai/litellm:main-stable

---

## Research Findings

### PostgreSQL Multiple Databases Best Practices
**Source**: [GitHub - mrts/docker-postgresql-multiple-databases](https://github.com/mrts/docker-postgresql-multiple-databases), [DEV Community Guide](https://dev.to/bgord/multiple-postgres-databases-in-a-single-docker-container-417l)

- ✅ Use initialization scripts in `/docker-entrypoint-initdb.d`
- ✅ Create separate databases with isolated users/passwords
- ✅ Efficient for dev/testing environments
- ⚠️ Scripts only run on first startup (empty volume)
- ⚠️ Production environments prefer separate containers for isolation

### Redis Multiple Databases Best Practices
**Source**: [Redis Official Docs](https://redis.io/docs/latest/develop/pubsub/), [Redis Docker Hub](https://hub.docker.com/_/redis), [Medium - Redis Pub/Sub Caching](https://osmos-tech-blog.medium.com/managing-in-memory-cache-invalidation-using-redis-pub-sub-c2bd60c13b69)

- ✅ Redis supports 16 databases (0-15) via SELECT command
- ✅ redis-stack-server includes: vector search, cache, pub/sub, JSON
- ✅ All databases share memory and configuration
- ✅ Use REDIS_DB environment variable to specify database number
- ⚠️ Protected mode disabled in Docker networks (ensure network isolation)

### Langfuse v3 Requirements
**Source**: [Langfuse Self-Hosting](https://langfuse.com/self-hosting), [Cache Configuration](https://langfuse.com/self-hosting/deployment/infrastructure/cache), [Docker Compose Guide](https://langfuse.com/self-hosting/deployment/docker-compose)

- ✅ PostgreSQL for application data
- ✅ Redis 7+ with `maxmemory-policy=noeviction` (CRITICAL)
- ✅ ClickHouse for analytics/tracing (v3 requirement)
- ✅ S3/MinIO for file uploads, events, exports
- ✅ Supports REDIS_DB for database selection
- ✅ Worker container for background processing

### LiteLLM Production Setup
**Source**: [LiteLLM Deploy Docs](https://docs.litellm.ai/docs/proxy/deploy), [Production Best Practices](https://docs.litellm.ai/docs/proxy/prod), [Docker Quick Start](https://docs.litellm.ai/docs/proxy/docker_quick_start)

- ✅ PostgreSQL for metadata/config storage
- ✅ Redis for caching and load balancing
- ✅ Separate Redis recommended for production (use REDIS_DB for dev)
- ✅ Requires LITELLM_MASTER_KEY and LITELLM_SALT_KEY
- ✅ Minimum 4 CPU cores, 8GB RAM for production

---

## Consolidation Strategy

### 1. PostgreSQL Consolidation
**Image**: `postgres:18.1` (NOT alpine - as per user requirement)

#### Database Structure
```sql
-- Database 1: main_db (Backend API)
CREATE DATABASE main_db;
CREATE USER main_user WITH PASSWORD 'CHANGE_ME_MAIN_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE main_db TO main_user;

-- Database 2: langfuse (Langfuse v3)
CREATE DATABASE langfuse;
CREATE USER langfuse WITH PASSWORD 'CHANGE_ME_LANGFUSE_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE langfuse TO langfuse;

-- Database 3: litellm (LiteLLM Proxy)
CREATE DATABASE litellm;
CREATE USER litellm WITH PASSWORD 'CHANGE_ME_LITELLM_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE litellm TO litellm;
```

#### Implementation
- Create `scripts/postgres-init/01-create-databases.sh`
- Mount script to `/docker-entrypoint-initdb.d/`
- Single volume: `postgres_data:/var/lib/postgresql/data`
- Port: 5432 (external + internal)

### 2. Redis Consolidation
**Image**: `redis/redis-stack-server:latest`

#### Database Allocation
```
DB 0: Main application (cache, vector search, pub/sub)
DB 1: Langfuse (queue, cache)
DB 2: LiteLLM (response cache, request deduplication)
DB 3-15: Reserved for future services
```

#### Configuration
```bash
redis-server \
  --maxmemory 1024mb \
  --maxmemory-policy noeviction \  # CRITICAL for Langfuse
  --appendonly yes \
  --save ""
```

#### Implementation
- Single volume: `redis_data:/data`
- Port: 6379 (external + internal)
- Services use REDIS_DB env var to select database

### 3. Service Connection Strings

#### Backend API
```env
DATABASE_URL=postgresql://main_user:CHANGE_ME_MAIN_PASSWORD@postgres:5432/main_db
REDIS_URL=redis://redis-stack:6379/0
```

#### Langfuse
```env
DATABASE_URL=postgresql://langfuse:CHANGE_ME_LANGFUSE_PASSWORD@postgres:5432/langfuse
REDIS_HOST=redis-stack
REDIS_PORT=6379
REDIS_DB=1
REDIS_AUTH=""
REDIS_CONNECTION_STRING=redis://redis-stack:6379/1
```

#### LiteLLM
```env
DATABASE_URL=postgresql://litellm:CHANGE_ME_LITELLM_PASSWORD@postgres:5432/litellm
REDIS_HOST=redis-stack
REDIS_PORT=6379
REDIS_DB=2
REDIS_PASSWORD=""
```

---

## Service Dependencies & Startup Order

### Layer 1: Infrastructure (no dependencies)
1. **postgres** (consolidated)
2. **redis-stack** (consolidated)
3. **mssql**

### Layer 2: Data & Analytics
4. **clickhouse** (requires: none)
5. **minio** (requires: none)
6. **minio-init** (requires: minio healthy)

### Layer 3: Observability & Gateway
7. **langfuse-web** (requires: postgres, redis-stack, clickhouse, minio-init)
8. **langfuse-worker** (requires: postgres, redis-stack, clickhouse, minio-init)
9. **litellm** (requires: postgres, redis-stack)

### Layer 4: Application Services
10. **backend** (requires: postgres, redis-stack, engine)
11. **engine** (requires: postgres, redis-stack, langfuse-web, litellm)

### Layer 5: Support Tools
12. **sqlpad** (requires: mssql)
13. **frontend** (requires: backend)

---

## Volume Management

### Consolidated Volumes
```yaml
volumes:
  # Consolidated Infrastructure
  postgres_data:           # Single PostgreSQL data (was 3 separate volumes)
  redis_data:              # Single Redis data (was 3 separate volumes)

  # Database Services
  mssql_data:
  mssql_logs:

  # Analytics & Storage
  clickhouse_data:
  clickhouse_logs:
  minio_data:

  # Tools
  sqlpad_data:
```

**Savings**: Reduced from 11 volumes to 8 volumes (3 volume reduction)

---

## Security Considerations

### Network Isolation
- All services in `chat_network` (bridge driver)
- Redis protected mode disabled (safe within Docker network)
- PostgreSQL password authentication required
- Engine only accessible from backend (CORS restriction)

### Credential Management
- All passwords in `.env` file (not committed to git)
- Separate users per database with minimal privileges
- LiteLLM SALT_KEY cannot be changed after initial setup
- Langfuse encryption keys must be persistent

### Port Exposure
- Frontend: 5173 (public)
- Backend: 8000 (public)
- Engine: 8001 (internal only via backend)
- PostgreSQL: 5432 (localhost only: 127.0.0.1:5432)
- Redis: 6379 (localhost only: 127.0.0.1:6379)
- LiteLLM: 4000 (public for direct access)
- Langfuse: 3000 (public for UI access)
- MinIO Console: 9091 (public for admin)
- SQLPad: 3010 (localhost only)

---

## Environment Variables Structure

### .env File Structure
```env
# === Mode Configuration ===
MODE=local  # local or dev

# === PostgreSQL (Consolidated) ===
POSTGRES_USER=postgres
POSTGRES_PASSWORD=CHANGE_ME_POSTGRES_PASSWORD
POSTGRES_DB=postgres

# Database Credentials
MAIN_DB_USER=main_user
MAIN_DB_PASSWORD=CHANGE_ME_MAIN_PASSWORD
MAIN_DB_NAME=main_db

LANGFUSE_DB_USER=langfuse
LANGFUSE_DB_PASSWORD=CHANGE_ME_LANGFUSE_PASSWORD
LANGFUSE_DB_NAME=langfuse

LITELLM_DB_USER=litellm
LITELLM_DB_PASSWORD=CHANGE_ME_LITELLM_PASSWORD
LITELLM_DB_NAME=litellm

# === Redis (Consolidated) ===
REDIS_PASSWORD=""  # Empty for development
REDIS_MAX_MEMORY=1024mb

# === MSSQL ===
MSSQL_SA_PASSWORD=CHANGE_ME_SQLSERVER_PASSWORD

# === ClickHouse ===
CLICKHOUSE_PASSWORD=CHANGE_ME_CLICKHOUSE_PASSWORD

# === MinIO ===
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=CHANGE_ME_MINIO_PASSWORD

# === Langfuse ===
LANGFUSE_NEXTAUTH_SECRET=<generate-random-32-char-string>
LANGFUSE_ENCRYPTION_KEY=<generate-random-32-char-string>
LANGFUSE_SALT=<generate-random-32-char-string>
LANGFUSE_INIT_USER_EMAIL=admin@example.com
LANGFUSE_INIT_USER_PASSWORD=CHANGE_ME_ADMIN_PASSWORD

# === LiteLLM ===
LITELLM_MASTER_KEY=CHANGE_ME_LITELLM_MASTER_KEY
LITELLM_SALT_KEY=CHANGE_ME_LITELLM_SALT_KEY
LITELLM_UI_USERNAME=admin
LITELLM_UI_PASSWORD=CHANGE_ME_LITELLM_UI_PASSWORD

# === Application ===
BACKEND_CORS_ORIGINS=["http://localhost:5173"]
ENGINE_CORS_ORIGINS=["http://localhost:8000","http://backend:8000"]
```

---

## Implementation Steps

### Phase 1: Infrastructure Setup (Days 1-2)
1. ✅ Create postgres init script (`scripts/postgres-init/01-create-databases.sh`)
2. ✅ Create consolidated docker-compose.yml
3. ✅ Configure postgres service with init script mount
4. ✅ Configure redis-stack with noeviction policy
5. ✅ Test postgres multi-database creation
6. ✅ Test redis multi-database access

### Phase 2: Supporting Services (Days 2-3)
7. ✅ Add MSSQL service with init scripts
8. ✅ Add ClickHouse service for Langfuse v3
9. ✅ Add MinIO service with bucket initialization
10. ✅ Add SQLPad service with MSSQL connection
11. ✅ Test all supporting services health checks

### Phase 3: Observability & Gateway (Days 3-4)
12. ✅ Add Langfuse web service with consolidated postgres/redis
13. ✅ Add Langfuse worker service
14. ✅ Add LiteLLM service with consolidated postgres/redis
15. ✅ Test Langfuse UI and tracing
16. ✅ Test LiteLLM proxy and UI

### Phase 4: Application Integration (Days 4-5)
17. ✅ Update backend to use consolidated postgres/redis
18. ✅ Update engine to use consolidated postgres/redis
19. ✅ Configure backend to use LiteLLM proxy
20. ✅ Configure backend/engine to use Langfuse tracing
21. ✅ Test end-to-end API flow with observability

### Phase 5: Testing & Documentation (Day 5)
22. ✅ Test `make run-dev` with all services
23. ✅ Test `make run-local` compatibility
24. ✅ Update README with service documentation
25. ✅ Create troubleshooting guide
26. ✅ Document environment variable configuration

---

## Testing Strategy

### Unit Tests
- Postgres init script creates all databases
- Redis accepts connections on all DB numbers (0, 1, 2)
- Each service can connect to its assigned database

### Integration Tests
- Backend → Postgres (main_db) read/write
- Backend → Redis (DB 0) cache operations
- Langfuse → Postgres (langfuse) + Redis (DB 1) + ClickHouse
- LiteLLM → Postgres (litellm) + Redis (DB 2)
- Full request flow: Frontend → Backend → Engine → LiteLLM → LLM API

### Health Check Tests
- All services return 200 on health endpoints
- Postgres accepts connections from all services
- Redis accepts connections from all services
- Dependency order respected (no startup failures)

---

## Rollback Plan

### If Consolidation Fails
1. Keep docker-compose.backup as reference
2. Restore separate postgres/redis instances per service
3. Update connection strings to point to separate instances
4. Roll back to previous volume structure

### Data Migration (if needed)
- Export data from consolidated postgres: `pg_dump`
- Import to separate instances: `psql`
- Redis data migration: `BGSAVE` + `redis-cli --rdb`

---

## Success Criteria

### Resource Efficiency
- ✅ Reduced from 3 postgres containers to 1
- ✅ Reduced from 3 redis containers to 1
- ✅ Reduced from 11 volumes to 8 volumes
- ✅ Lower memory footprint (estimate: -2GB RAM)

### Functionality
- ✅ All services healthy on startup
- ✅ Backend API functional with postgres/redis
- ✅ Langfuse tracing operational
- ✅ LiteLLM proxy operational
- ✅ End-to-end chat flow working

### Maintainability
- ✅ Single postgres instance to backup
- ✅ Single redis instance to monitor
- ✅ Clear database/DB number separation
- ✅ Documented configuration in .env

---

## Open Questions & Decisions Needed

1. **PostgreSQL Version**: Use `postgres:18.1` (not alpine) - ✅ CONFIRMED by user
2. **Redis Memory Limit**: 1024mb sufficient for 3 services? - ⚠️ NEEDS VALIDATION
3. **Backup Strategy**: Do we need pg_dump cron job? - ⚠️ NEEDS DECISION
4. **Production Migration**: Is this for dev only or production too? - ⚠️ NEEDS CLARIFICATION
5. **Neo4j**: Not in required services list - removed? - ⚠️ NEEDS CONFIRMATION

---

## Next Steps

1. **Review this plan** with stakeholders
2. **Validate assumptions** (memory limits, DB numbers, etc.)
3. **Get approval** to proceed with implementation
4. **Create todo checklist** from implementation steps
5. **Begin Phase 1** (Infrastructure Setup)

---

## References

### PostgreSQL
- [GitHub - Multiple PostgreSQL Databases](https://github.com/mrts/docker-postgresql-multiple-databases)
- [DEV Community - Multiple Postgres Databases](https://dev.to/bgord/multiple-postgres-databases-in-a-single-docker-container-417l)
- [CommandPrompt - Multiple Postgres Databases](https://www.commandprompt.com/education/how-to-include-multiple-postgres-databases-in-a-single-docker-container/)

### Redis
- [Redis Official Docs - Pub/Sub](https://redis.io/docs/latest/develop/pubsub/)
- [Redis Docker Hub](https://hub.docker.com/_/redis)
- [Medium - Redis Pub/Sub Caching](https://osmos-tech-blog.medium.com/managing-in-memory-cache-invalidation-using-redis-pub-sub-c2bd60c13b69)

### Langfuse
- [Langfuse Self-Hosting](https://langfuse.com/self-hosting)
- [Cache Configuration](https://langfuse.com/self-hosting/deployment/infrastructure/cache)
- [Docker Compose Guide](https://langfuse.com/self-hosting/deployment/docker-compose)

### LiteLLM
- [LiteLLM Deploy Docs](https://docs.litellm.ai/docs/proxy/deploy)
- [Production Best Practices](https://docs.litellm.ai/docs/proxy/prod)
- [Docker Quick Start](https://docs.litellm.ai/docs/proxy/docker_quick_start)
