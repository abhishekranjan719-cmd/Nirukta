# Troubleshooting Guide

Comprehensive troubleshooting guide for the consolidated infrastructure.

## Table of Contents

- [Quick Diagnostics](#quick-diagnostics)
- [Common Issues](#common-issues)
- [Service-Specific Issues](#service-specific-issues)
- [Database Issues](#database-issues)
- [Network Issues](#network-issues)
- [Performance Issues](#performance-issues)
- [Recovery Procedures](#recovery-procedures)

---

## Quick Diagnostics

### Check All Services Status

```bash
docker ps --filter "name=chat-" --format "table {{.Names}}\t{{.Status}}"
```

### Check All Health Endpoints

```bash
echo "Backend:" && curl -s http://localhost:8000/health | jq .
echo "Engine:" && curl -s http://localhost:8001/health | jq .
echo "Langfuse:" && curl -s http://localhost:3000/api/public/health | jq .
echo "LiteLLM:" && curl -s http://localhost:4000/health/liveliness
```

### Check Docker Logs

```bash
# Recent logs from all services
docker-compose logs --tail=50 --follow

# Specific service
docker logs chat-backend --tail=100
docker logs chat-engine --tail=100
docker logs chat-langfuse-web --tail=100
docker logs chat-litellm --tail=100
```

### Check Docker Network

```bash
docker network inspect chat_network
```

### Check Volumes

```bash
docker volume ls | grep "^z_"
```

---

## Common Issues

### Issue 1: Services Won't Start

**Symptoms:**
```
dependency failed to start: container chat-xxx is unhealthy
```

**Diagnosis:**
```bash
# Check which service is unhealthy
docker ps -a --filter "name=chat-"

# Check logs of unhealthy service
docker logs chat-[service-name] --tail=100
```

**Solutions:**

1. **Check dependencies are running:**
   ```bash
   # PostgreSQL must be healthy
   docker exec chat-postgres pg_isready -U postgres

   # Redis must be responding
   docker exec chat-redis-stack redis-cli ping
   ```

2. **Restart in correct order:**
   ```bash
   # Stop all
   docker-compose down

   # Start layer by layer
   docker-compose up -d postgres redis-stack mssql
   sleep 10
   docker-compose up -d clickhouse minio minio-init
   sleep 10
   docker-compose up -d langfuse-web langfuse-worker litellm
   sleep 10
   docker-compose up -d backend engine frontend
   ```

3. **Check .env file exists and is populated:**
   ```bash
   ls -la .env
   grep "LANGFUSE_ENCRYPTION_KEY" .env
   grep "LITELLM_MASTER_KEY" .env
   ```

---

### Issue 2: PostgreSQL Init Scripts Not Running

**Symptoms:**
- Databases `main_db`, `langfuse`, `litellm` don't exist
- Services can't connect to PostgreSQL

**Diagnosis:**
```bash
# Check if databases exist
docker exec chat-postgres psql -U postgres -c "\l"
```

**Solution:**

Init scripts only run on **first startup** with empty volume:

```bash
# Stop and remove everything
docker-compose down -v  # ⚠️ Deletes all data!

# Start fresh
docker-compose up -d postgres

# Wait for initialization
docker logs chat-postgres --follow
# Look for: "✅ All databases created successfully!"

# Verify databases
docker exec chat-postgres psql -U postgres -c "\l"
```

**Alternative - Manual Database Creation:**
```bash
docker exec chat-postgres psql -U postgres -c "
CREATE DATABASE main_db OWNER main_user;
CREATE DATABASE langfuse OWNER langfuse;
CREATE DATABASE litellm OWNER litellm;
"
```

---

### Issue 3: Redis Connection Errors

**Symptoms:**
```
DENIED Redis is running in protected mode
ReplyError: DENIED
Connection refused to redis-stack:6379
```

**Diagnosis:**
```bash
# Check Redis is running
docker exec chat-redis-stack redis-cli ping

# Check Redis config
docker exec chat-redis-stack redis-cli CONFIG GET protected-mode
```

**Solution:**

1. **Verify Redis configuration in docker-compose.yml:**
   ```yaml
   redis-stack:
     command: >
       redis-server
       --protected-mode no  # Must be disabled for Docker network
       --maxmemory 1024mb
       --maxmemory-policy noeviction
   ```

2. **Restart Redis:**
   ```bash
   docker-compose restart redis-stack
   ```

3. **Verify connection from services:**
   ```bash
   docker exec chat-backend python -c "
   import redis
   r = redis.Redis(host='redis-stack', port=6379, db=0)
   print(r.ping())
   "
   ```

---

### Issue 4: Langfuse "Invalid Environment Variables"

**Symptoms:**
```
❌ Invalid environment variables: {
  ENCRYPTION_KEY: ['ENCRYPTION_KEY must be 256 bits, 64 string characters in hex format']
}
```

**Diagnosis:**
```bash
# Check encryption key length
docker exec chat-langfuse-web env | grep ENCRYPTION_KEY | wc -c
# Should be 64 hex characters (+ variable name)
```

**Solution:**

1. **Generate proper keys:**
   ```bash
   echo "LANGFUSE_NEXTAUTH_SECRET=$(openssl rand -hex 32)" >> .env
   echo "LANGFUSE_ENCRYPTION_KEY=$(openssl rand -hex 32)" >> .env
   echo "LANGFUSE_SALT=$(openssl rand -hex 32)" >> .env
   ```

2. **Recreate container (force reload .env):**
   ```bash
   docker-compose up -d --force-recreate langfuse-web
   ```

3. **Verify inside container:**
   ```bash
   docker exec chat-langfuse-web env | grep LANGFUSE_ENCRYPTION_KEY
   ```

---

### Issue 5: Langfuse Health Check Failing

**Symptoms:**
- Container status shows `(unhealthy)` or `(starting)`
- Health check endpoint returns error
- Other services can't start due to dependency

**Diagnosis:**
```bash
# Check container status
docker ps --filter "name=chat-langfuse-web"

# Test health check from inside container
docker exec chat-langfuse-web wget --quiet --tries=1 --spider http://127.0.0.1:3000/api/public/health && echo "OK" || echo "FAIL"

# Test from host
curl -s http://localhost:3000/api/public/health | jq .
```

**Solutions:**

1. **Langfuse is running but health check uses wrong URL:**

   The fix in docker-compose.yml:
   ```yaml
   healthcheck:
     test: ["CMD-SHELL", "wget --quiet --tries=1 --spider http://127.0.0.1:3000/api/public/health || exit 1"]
   ```

   **Not:** `http://localhost:3000` (doesn't resolve in container)

2. **Langfuse needs time to initialize:**
   ```yaml
   healthcheck:
     start_period: 60s  # Give 60 seconds before health checks start
     retries: 15        # More retries
   ```

3. **Check Langfuse logs for actual errors:**
   ```bash
   docker logs chat-langfuse-web --tail=100
   ```

4. **If API works but health check fails, start services without health dependency:**
   ```bash
   docker-compose up -d --no-deps backend engine
   ```

---

### Issue 6: LiteLLM Authentication Errors

**Symptoms:**
```
{
  "error": {
    "message": "Authentication Error, No api key passed in.",
    "type": "auth_error",
    "code": "401"
  }
}
```

**Diagnosis:**
```bash
# Test without auth (should fail)
curl http://localhost:4000/health

# Test with auth
curl -H "Authorization: Bearer sk-1234567890abcdef" http://localhost:4000/health
```

**Solution:**

LiteLLM requires authentication on most endpoints except `/health/liveliness`:

```bash
# Test liveliness (no auth required)
curl http://localhost:4000/health/liveliness

# Test with proper auth
LITELLM_KEY=$(grep LITELLM_MASTER_KEY .env | cut -d'=' -f2)
curl -H "Authorization: Bearer $LITELLM_KEY" http://localhost:4000/health
```

**For API calls:**
```python
import httpx

client = httpx.Client()
response = client.get(
    "http://localhost:4000/v1/models",
    headers={"Authorization": f"Bearer {LITELLM_MASTER_KEY}"}
)
```

---

### Issue 7: LiteLLM Config Not Loading

**Symptoms:**
- LiteLLM starts but models not available
- Config changes not taking effect

**Diagnosis:**
```bash
# Check if config file is mounted
docker exec chat-litellm ls -la /app/config.yaml

# Check config syntax
docker exec chat-litellm cat /app/config.yaml | head -50
```

**Solution:**

1. **Verify docker-compose.yml has config mount:**
   ```yaml
   litellm:
     volumes:
       - ./configs/litellm/config.yaml:/app/config.yaml:ro
     command: ["--config", "/app/config.yaml", "--port", "4000"]
   ```

2. **Check config.yaml syntax:**
   ```bash
   # Validate YAML
   python3 -c "import yaml; yaml.safe_load(open('configs/litellm/config.yaml'))"
   ```

3. **Restart with config:**
   ```bash
   docker-compose restart litellm
   docker logs chat-litellm --tail=50 | grep -i config
   ```

---

### Issue 8: Frontend Can't Connect to Backend

**Symptoms:**
- Frontend shows network errors
- CORS errors in browser console
- Backend API not responding

**Diagnosis:**
```bash
# Test backend from host
curl http://localhost:8000/health

# Check backend logs for CORS errors
docker logs chat-backend --tail=50 | grep -i cors

# Verify frontend env var
docker exec chat-frontend env | grep VITE_BACKEND_URL
```

**Solution:**

1. **Check CORS configuration in `.env`:**
   ```bash
   BACKEND_CORS_ORIGINS=["http://localhost:5173"]
   ```

2. **Verify backend is accessible:**
   ```bash
   curl -v http://localhost:8000/health
   ```

3. **Check browser console for actual error:**
   - Open DevTools → Network tab
   - Look for failed requests to backend

4. **Restart backend if CORS config changed:**
   ```bash
   docker-compose restart backend
   ```

---

### Issue 9: Backend Can't Connect to Engine

**Symptoms:**
```
Connection refused to engine:8001
Engine service unavailable
```

**Diagnosis:**
```bash
# Check engine is running
docker ps --filter "name=chat-engine"

# Test engine health
curl http://localhost:8001/health

# Check if backend can reach engine
docker exec chat-backend curl -s http://engine:8001/health
```

**Solution:**

1. **Verify both are in same network:**
   ```bash
   docker inspect chat-backend | grep NetworkMode
   docker inspect chat-engine | grep NetworkMode
   # Both should be in chat_network
   ```

2. **Check ENGINE_URL in backend settings:**
   ```bash
   docker exec chat-backend python -c "from app.config import settings; print(settings.engine_url)"
   # Should be: http://engine:8001
   ```

3. **Restart backend after engine is healthy:**
   ```bash
   docker-compose restart engine
   sleep 5
   docker-compose restart backend
   ```

---

## Service-Specific Issues

### PostgreSQL Issues

**Can't connect:**
```bash
# Check if running
docker exec chat-postgres pg_isready -U postgres

# Check port binding
docker port chat-postgres

# Connect manually
docker exec -it chat-postgres psql -U postgres
```

**Database doesn't exist:**
```sql
-- List all databases
\l

-- Create database
CREATE DATABASE main_db OWNER main_user;
```

**Permission denied:**
```sql
-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE main_db TO main_user;
\c main_db
GRANT ALL ON SCHEMA public TO main_user;
```

---

### Redis Issues

**Memory issues:**
```bash
# Check memory usage
docker exec chat-redis-stack redis-cli INFO memory

# Check eviction policy
docker exec chat-redis-stack redis-cli CONFIG GET maxmemory-policy
# Should be: noeviction (for Langfuse)
```

**Database selection:**
```bash
# Test different databases
docker exec chat-redis-stack redis-cli -n 0 PING  # Main (DB 0)
docker exec chat-redis-stack redis-cli -n 1 PING  # Langfuse (DB 1)
docker exec chat-redis-stack redis-cli -n 2 PING  # LiteLLM (DB 2)
```

---

### ClickHouse Issues

**Connection refused:**
```bash
# Check if running
docker exec chat-clickhouse clickhouse-client --query "SELECT 1"

# Check Langfuse can connect
docker exec chat-langfuse-web wget -qO- http://clickhouse:8123/ping
```

**Database migration errors:**
```bash
# Check migration status
docker logs chat-langfuse-web | grep -i clickhouse

# Manual migration (if needed)
docker exec chat-langfuse-web npm run db:migrate:clickhouse
```

---

### MinIO Issues

**Bucket doesn't exist:**
```bash
# List buckets
docker exec chat-minio mc ls local/

# Create bucket manually
docker exec chat-minio mc mb local/langfuse
```

**Access denied:**
```bash
# Set public policy (dev only!)
docker exec chat-minio mc policy set download local/langfuse
```

---

## Database Issues

### PostgreSQL Volume Mount Error (18+)

**Symptom:**
```
PostgreSQL 18.1 - there appears to be PostgreSQL data in:
  /var/lib/postgresql/data (unused mount/volume)
```

**Solution:**

PostgreSQL 18+ requires volume mount at `/var/lib/postgresql` not `/var/lib/postgresql/data`:

```yaml
volumes:
  - postgres_data:/var/lib/postgresql  # Correct for 18+
  # NOT /var/lib/postgresql/data
```

---

### Database Connection Pool Exhausted

**Symptoms:**
- "Too many connections" errors
- Slow query performance
- Service timeouts

**Solution:**

1. **Check connection count:**
   ```sql
   SELECT count(*) FROM pg_stat_activity;
   ```

2. **Increase max connections in PostgreSQL:**
   ```bash
   docker exec chat-postgres psql -U postgres -c "ALTER SYSTEM SET max_connections = 200;"
   docker-compose restart postgres
   ```

3. **Adjust application pool sizes in settings.py**

---

## Network Issues

### Services Can't Communicate

**Diagnosis:**
```bash
# All services should be in chat_network
docker network inspect chat_network | jq '.[0].Containers'

# Test connectivity between services
docker exec chat-backend ping -c 2 engine
docker exec chat-backend ping -c 2 postgres
docker exec chat-backend ping -c 2 redis-stack
```

**Solution:**

1. **Recreate network:**
   ```bash
   docker-compose down
   docker network rm chat_network
   docker-compose up -d
   ```

2. **Verify DNS resolution:**
   ```bash
   docker exec chat-backend nslookup engine
   docker exec chat-backend nslookup postgres
   ```

---

### Port Already in Use

**Symptoms:**
```
Error starting userland proxy: listen tcp4 0.0.0.0:8000: bind: address already in use
```

**Solution:**

1. **Find process using port:**
   ```bash
   lsof -i :8000
   # or
   netstat -tulpn | grep 8000
   ```

2. **Kill process or change port in docker-compose.yml:**
   ```yaml
   ports:
     - "8001:8000"  # Map to different host port
   ```

---

## Performance Issues

### High Memory Usage

**Diagnosis:**
```bash
# Check container resource usage
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Check Redis memory
docker exec chat-redis-stack redis-cli INFO memory | grep used_memory_human
```

**Solution:**

1. **Adjust Redis max memory:**
   ```yaml
   redis-stack:
     command: >
       redis-server
       --maxmemory 2048mb  # Increase from 1024mb
   ```

2. **Set resource limits in docker-compose.yml:**
   ```yaml
   deploy:
     resources:
       limits:
         memory: 2G
       reservations:
         memory: 1G
   ```

---

### Slow Database Queries

**Diagnosis:**
```sql
-- Check slow queries
SELECT query, calls, mean_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

**Solution:**

1. **Add indexes**
2. **Analyze query plans:** `EXPLAIN ANALYZE <query>`
3. **Increase shared buffers**

---

## Recovery Procedures

### Complete Reset (Nuclear Option)

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

---

### Partial Reset (Keep Data)

```bash
# Stop services
docker-compose down

# Keep volumes, restart services
docker-compose up -d
```

---

### Restore from Backup

**PostgreSQL:**
```bash
# Restore all databases
cat backup.sql | docker exec -i chat-postgres psql -U postgres

# Restore specific database
cat main_db_backup.sql | docker exec -i chat-postgres psql -U main_user main_db
```

**Redis:**
```bash
# Stop Redis
docker-compose stop redis-stack

# Copy backup
docker cp redis_backup.rdb chat-redis-stack:/data/dump.rdb

# Start Redis
docker-compose start redis-stack
```

---

### Service Won't Stop

```bash
# Force kill
docker kill chat-[service-name]

# Remove container
docker rm -f chat-[service-name]

# Recreate
docker-compose up -d [service-name]
```

---

## Getting Help

### Collect Diagnostics

```bash
# Save diagnostic info
cat > diagnostics.txt <<EOF
=== Docker Version ===
$(docker version)

=== Docker Compose Version ===
$(docker-compose version)

=== Service Status ===
$(docker ps --filter "name=chat-")

=== Recent Logs ===
$(docker-compose logs --tail=50)

=== Network Info ===
$(docker network inspect chat_network)

=== Volume Info ===
$(docker volume ls | grep "^z_")
EOF
```

### Check Logs

```bash
# All services
docker-compose logs --tail=100 > all_logs.txt

# Specific service with timestamps
docker logs chat-backend --timestamps --tail=500 > backend_logs.txt
```

---

**Last Updated:** 2025-12-31
**Version:** 1.0.0
