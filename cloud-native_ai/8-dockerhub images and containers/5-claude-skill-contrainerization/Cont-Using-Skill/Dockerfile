# === Stage 1: Base ===
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# === Stage 2: Builder (Dependencies with UV) ===
FROM base AS builder

# Install system dependencies for psycopg2 (PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies with caching
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# === Stage 3: Development/Test ===
FROM base AS dev

# Install system dependencies for psycopg2 (PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY . .

# Neon DB environment variable (passed at runtime)
# DATABASE_URL should be passed via: docker run -e DB_URL="postgresql://..."
ENV DB_URL=""

# Run tests (uncomment as needed)
# RUN uv run pytest

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# === Stage 4: Production ===
FROM python:3.11-slim AS production

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for psycopg2 (PostgreSQL) runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN adduser --disabled-password --no-create-home appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy application source
COPY . .

# Neon DB environment variable (passed at runtime)
# For Neon PostgreSQL, use NullPool - let Neon's pooler handle connections
# DATABASE_URL should be passed via: docker run -e DB_URL="postgresql://..."
ENV DB_URL=""

# Set ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose application port
EXPOSE 8000

# Labels
LABEL NAME="cont-using-skill" \
      VERSION="1.0.0" \
      DESCRIPTION="FastAPI Todo API with Neon PostgreSQL" \
      AUTHOR="Ali Jilani" \
      DATABASE="Neon PostgreSQL"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/docs')" || exit 1

# Application entrypoint (production - no reload)
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
