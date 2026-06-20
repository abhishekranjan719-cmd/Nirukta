FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY engine/pyproject.toml ./

# Create lock file if it doesn't exist and install dependencies
RUN uv sync || uv pip install -e .

# Copy configs folder (required for centralized settings)
COPY configs /configs

# Copy prompts folder (required for formatter system prompt)
COPY prompts /app/prompts

# Copy application code
COPY engine/app ./app

# Expose port
EXPOSE 8001

# Run the application
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
