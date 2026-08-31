FROM python:3.13-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install dependencies first (better Docker layer caching)
COPY pyproject.toml uv.lock README.md ./

RUN uv sync --frozen --no-dev

COPY alembic ./alembic
COPY alembic.ini ./

# Copy application source
COPY app ./app


FROM python:3.13-slim AS runtime

WORKDIR /app

# Copy the virtual environment and application
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/alembic /app/alembic
COPY --from=builder /app/alembic.ini /app/alembic.ini
COPY --from=builder /app/app /app/app

# Make the virtual environment the default Python environment
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
