  ---

  Multi-Stage Docker Build Architecture

  Stage 1: Builder Stage

  Purpose: Install dependencies and compile packages in an isolated environment

  FROM python:3.12-slim AS builder

# Install uv for fast dependency management

  COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Environment optimizations

  ENV UV_LINK_MODE=copy \
      UV_COMPILE_BYTECODE=1

  WORKDIR /app

# Copy dependency files first (layer caching)

  COPY pyproject.toml uv.lock ./

# Install dependencies with cache mount

  RUN --mount=type=cache,target=/root/.cache/uv \
      uv sync --locked --no-dev --no-editable

  Stage 2: Runtime/Production Stage

  Purpose: Minimal image with only runtime artifacts

  FROM python:3.12-slim AS runtime

# Create non-root user for security

  RUN useradd --create-home --shell /bin/bash app

  WORKDIR /app

# Copy only the virtual environment from builder

  COPY --from=builder --chown=app:app /app/.venv /app/.venv

# Copy application code

  COPY --chown=app:app ./app ./app

# Use non-root user

  USER app

# Set PATH to use venv

  ENV PATH="/app/.venv/bin:$PATH"

  CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]

  ---

  Key Optimization Strategies

| Strategy                  | Benefit                                        |
| ------------------------- | ---------------------------------------------- |
| Separate dependency layer | Dependency changes cached separately from code |
| UV cache mounts           | 50-70% faster builds across iterations         |
| UV_COMPILE_BYTECODE=1     | Faster application startup (pre-compiled .pyc) |
| Non-root user             | Reduced attack surface                         |
| Slim base image           | Smaller final image (~50% reduction)           |
| --no-dev --locked         | Production-only deps, exact versions           |

  ---

  Neon Database Connection Best Practices

  For SQLModel with Neon PostgreSQL:

  from sqlmodel import SQLModel
  from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
  from sqlalchemy.pool import NullPool

# Use NullPool + Neon's PgBouncer for production

  engine = create_async_engine(
      "postgresql+asyncpg://user:pass@ep-xxx.neon.tech/db?sslmode=require",
      poolclass=NullPool,  # Let Neon's PgBouncer handle pooling
      pool_pre_ping=True,  # Handle stale connections
  )

  Important: Use direct connection (not pooled) for Alembic migrations.

  ---

  Optional Stage 3: Testing Stage (CI/CD)

  FROM builder AS testing

  RUN --mount=type=cache,target=/root/.cache/uv \
      uv sync --locked  # Include dev dependencies

  COPY --chown=app:app . .

  CMD ["pytest", "-v"]

  ---

  Summary of Stages

| Stage   | Base Image        | Contains                      | Size                               |
| ------- | ----------------- | ----------------------------- | ---------------------------------- |
| Builder | python:3.12-slim  | uv, build tools, dependencies | ~400MB                             |
| Runtime | python:3.12-slim  | .venv + app code only         | ~150MB                             |
| Testing | (extends builder) | + pytest, dev tools           | ~450MB |
