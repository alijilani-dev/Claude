# ==============================================================================
# BUILDER STAGE
# ==============================================================================
FROM python:3.14-slim AS builder

# Optimized way to get 'uv' without using pip
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Ensure uv doesn't try to use hard links in the cache mount
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

# Copy only dependency files to leverage layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies into a virtual environment
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# Copy the rest of your source code
COPY . .

# Environment for the build context
ENV PATH="/app/.venv/bin:$PATH"

# ==============================================================================
# PRODUCTION STAGE
# ==============================================================================
FROM python:3.14-slim AS production

WORKDIR /app

# Create non-root user for security
RUN groupadd --gid 1000 app && \
    useradd --uid 1000 --gid app --shell /bin/bash --create-home app

# Copy ONLY the virtual environment and your app source from builder
COPY --from=builder /app/.venv /app/.venv
COPY --chown=app:app src/ /app/src/

# Set production environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src"

USER app

EXPOSE 8000

# Health check using the internal port
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Launch the app (matching your folder structure)
CMD ["uvicorn", "progress_tracker.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]