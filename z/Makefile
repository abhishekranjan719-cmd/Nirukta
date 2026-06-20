.PHONY: help setup up down logs logs-backend logs-engine logs-frontend test test-backend test-engine test-integration clean rebuild run-dev run-local run-dev-tests run-local-tests stop-local

help:
	@echo "Zuna - Development Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup              Install all dependencies (frontend, backend, engine)"
	@echo ""
	@echo "Run Modes:"
	@echo "  make run-dev            Run all services in Docker (docker-compose)"
	@echo "  make run-local          Run all services locally (uv venv from project root)"
	@echo "  make stop-local         Stop all locally running services"
	@echo ""
	@echo "Testing:"
	@echo "  make run-dev-tests      Run tests against Docker services"
	@echo "  make run-local-tests    Run tests against local services"
	@echo "  make test               Run unit tests (backend + engine)"
	@echo "  make test-backend       Run backend tests"
	@echo "  make test-engine        Run engine tests"
	@echo "  make test-integration   Run integration tests"
	@echo ""
	@echo "Docker Commands:"
	@echo "  make up                 Start all services with docker-compose"
	@echo "  make down               Stop all services"
	@echo "  make rebuild            Rebuild and restart all services"
	@echo "  make logs               View logs from all services"
	@echo "  make logs-backend       View backend logs"
	@echo "  make logs-engine        View engine logs"
	@echo "  make logs-frontend      View frontend logs"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean              Remove containers, volumes, and dependencies"

setup:
	@echo "📦 Installing all dependencies..."
	@echo ""
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo ""
	@echo "Installing backend dependencies..."
	cd backend && uv sync
	@echo ""
	@echo "Installing engine dependencies..."
	cd engine && uv sync
	@echo ""
	@echo "✅ Setup complete!"

# ============================================================================
# RUN DEV - Docker Compose
# ============================================================================

run-dev:
	@echo "🐳 Starting all services in Docker..."
	@echo ""
	docker-compose up -d
	@echo ""
	@echo "⏳ Waiting for services to be healthy..."
	@sleep 5
	@echo ""
	@echo "✅ Services started in Docker mode!"
	@echo ""
	@echo "📍 Service URLs:"
	@echo "  Frontend:    http://localhost:5173"
	@echo "  Backend API: http://localhost:8000/docs"
	@echo "  Engine API:  http://localhost:8001/docs"
	@echo ""
	@echo "📊 View logs: make logs"
	@echo "🛑 Stop:      make down"

# ============================================================================
# RUN LOCAL - Local uv venv
# ============================================================================

run-local:
	@echo "🖥️  Starting all services locally (uv venv)..."
	@echo ""
	@echo "Checking dependencies..."
	@if [ ! -d "backend/.venv" ] || [ ! -d "engine/.venv" ] || [ ! -d "frontend/node_modules" ]; then \
		echo "❌ Dependencies not installed. Running 'make setup'..."; \
		make setup; \
	fi
	@mkdir -p logs
	@echo ""
	@echo "✅ Starting services in background..."
	@echo ""
	@echo "🔧 Starting Engine on port 8001..."
	@cd engine && uv run uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload > $(CURDIR)/logs/engine.log 2>&1 & echo $$! > $(CURDIR)/logs/engine.pid
	@sleep 2
	@echo "🔧 Starting Backend on port 8000..."
	@cd backend && BACKEND_ENGINE_URL=http://localhost:8001 uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > $(CURDIR)/logs/backend.log 2>&1 & echo $$! > $(CURDIR)/logs/backend.pid
	@sleep 2
	@echo "🔧 Starting Frontend on port 5173..."
	@cd frontend && VITE_BACKEND_URL=http://localhost:8000 npm run dev > $(CURDIR)/logs/frontend.log 2>&1 & echo $$! > $(CURDIR)/logs/frontend.pid
	@sleep 3
	@echo ""
	@echo "✅ All services started locally!"
	@echo ""
	@echo "📍 Service URLs:"
	@echo "  Frontend:    http://localhost:5173"
	@echo "  Backend API: http://localhost:8000/docs"
	@echo "  Engine API:  http://localhost:8001/docs"
	@echo ""
	@echo "📊 View logs:"
	@echo "  Engine:   tail -f logs/engine.log"
	@echo "  Backend:  tail -f logs/backend.log"
	@echo "  Frontend: tail -f logs/frontend.log"
	@echo ""
	@echo "🛑 Stop:      make stop-local"

stop-local:
	@echo "🛑 Stopping all local services..."
	@if [ -f logs/frontend.pid ]; then \
		kill $$(cat logs/frontend.pid) 2>/dev/null || true; \
		rm logs/frontend.pid; \
		echo "✅ Frontend stopped"; \
	fi
	@if [ -f logs/backend.pid ]; then \
		kill $$(cat logs/backend.pid) 2>/dev/null || true; \
		rm logs/backend.pid; \
		echo "✅ Backend stopped"; \
	fi
	@if [ -f logs/engine.pid ]; then \
		kill $$(cat logs/engine.pid) 2>/dev/null || true; \
		rm logs/engine.pid; \
		echo "✅ Engine stopped"; \
	fi
	@echo ""
	@echo "✅ All local services stopped!"

# ============================================================================
# TESTING
# ============================================================================

run-dev-tests:
	@echo "🧪 Running tests against Docker services..."
	@echo ""
	@echo "Checking if Docker services are running..."
	@if ! docker-compose ps | grep -q "Up"; then \
		echo "❌ Docker services not running. Starting them..."; \
		make run-dev; \
		sleep 10; \
	fi
	@echo ""
	@echo "✅ Docker services are running"
	@echo ""
	@echo "Running unit tests..."
	@echo ""
	@echo "📦 Backend unit tests..."
	@cd backend && uv run pytest -v --tb=short
	@echo ""
	@echo "⚙️  Engine unit tests..."
	@cd engine && uv run pytest -v --tb=short
	@echo ""
	@echo "🔗 Integration tests (Docker environment)..."
	@cd backend && uv run pytest ../tests/integration/ -v --tb=short
	@echo ""
	@echo "✅ All dev tests completed!"

run-local-tests:
	@echo "🧪 Running tests against local services..."
	@echo ""
	@echo "Checking if local services are running..."
	@if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then \
		echo "❌ Local services not running. Please start them with 'make run-local'"; \
		exit 1; \
	fi
	@echo ""
	@echo "✅ Local services are running"
	@echo ""
	@echo "Running unit tests..."
	@echo ""
	@echo "📦 Backend unit tests..."
	@cd backend && uv run pytest -v --tb=short
	@echo ""
	@echo "⚙️  Engine unit tests..."
	@cd engine && uv run pytest -v --tb=short
	@echo ""
	@echo "🔗 Integration tests (local environment)..."
	@cd backend && uv run pytest ../tests/integration/ -v --tb=short
	@echo ""
	@echo "✅ All local tests completed!"

test: test-backend test-engine
	@echo ""
	@echo "✅ All unit tests completed!"

test-backend:
	@echo "📦 Running backend tests..."
	@cd backend && uv run pytest -v

test-engine:
	@echo "⚙️  Running engine tests..."
	@cd engine && uv run pytest -v

test-integration:
	@echo "🔗 Running integration tests..."
	@echo "Note: Requires services to be running (make run-dev or make run-local)"
	@cd backend && uv run pytest ../tests/integration/ -v

# ============================================================================
# DOCKER COMMANDS
# ============================================================================

up:
	@echo "Starting all services..."
	docker-compose up -d
	@echo ""
	@echo "Services starting..."
	@echo "Frontend: http://localhost:5173"
	@echo "Backend API: http://localhost:8000/docs"
	@echo "Engine API: http://localhost:8001/docs"
	@echo ""
	@echo "Run 'make logs' to view logs"

down:
	@echo "Stopping all services..."
	docker-compose down

rebuild:
	@echo "Rebuilding and restarting services..."
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d
	@echo "Services rebuilt and started!"

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-engine:
	docker-compose logs -f engine

logs-frontend:
	docker-compose logs -f frontend

# ============================================================================
# MAINTENANCE
# ============================================================================

clean:
	@echo "Cleaning up..."
	docker-compose down -v
	rm -rf frontend/node_modules
	rm -rf backend/.venv
	rm -rf engine/.venv
	rm -rf logs/*.log
	rm -rf logs/*.pid
	@echo "Cleanup complete!"
