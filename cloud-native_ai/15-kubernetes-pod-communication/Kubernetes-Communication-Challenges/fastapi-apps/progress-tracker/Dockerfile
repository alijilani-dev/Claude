




FROM python:3.14-slim AS builder

WORKDIR /app

# Install uv for fast dependency management
RUN pip install uv

# Copy dependency files first (cache layer)
COPY pyproject.toml uv.lock ./

# Install dependencies into virtual environment
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project




FROM python:3.14-slim AS builder

WORKDIR /app

# Install uv for fast dependency management
RUN pip install uv

# Copy dependency files first (cache layer)
COPY pyproject.toml uv.lock ./

# Install dependencies into virtual environment
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# Copy application code
COPY . .

# Environment for development
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

# Development runs with --reload for hot reloading
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

# ==============================================================================
# PRODUCTION STAGE - Minimal secure runtime
# ==============================================================================
FROM python:3.14-slim AS production

WORKDIR /app

# Create non-root user
RUN groupadd --gid 1000 app && \
    useradd --uid 1000 --gid app --shell /bin/bash --create-home app

# Copy Virtual Environment from Builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code
#COPY --chown=app:app src/progress_tracker/main.py ./
# This copies the entire src folder's contents into /app
COPY --chown=app:app src/ ./

# Set environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/app/.venv/bin:$PATH"

# Switch to non-root user
USER app

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Production runs with multiple workers and graceful shutdown
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--timeout-graceful-shutdown", "30"]

# Change "main:app" to "folder_name.main:app"
# CMD ["uvicorn", "progress_tracker.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

# Change "main:app" to "folder_name.main:app"
CMD ["uvicorn", "progress_tracker.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--timeout-graceful-shutdown", "30"]