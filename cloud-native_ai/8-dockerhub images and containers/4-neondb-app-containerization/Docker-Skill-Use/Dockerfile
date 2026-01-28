FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

EXPOSE 8000

LABEL   NAME="Docker-Skill-Use" \
        VERSION="1.0.0" \
        DESCRIPTION="A simple Docker Hub Test application for image upload to docker hub" \
        AUTHOR="Ali Jilani"

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]