# syntax=docker/dockerfile:1

FROM python:3.12-slim

ENV PYTHONPATH=/app/src \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TMPDIR=/input_data

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY src ./src
RUN mkdir -p /input_data

# Any args passed to docker run get forwarded to __main__.py
ENTRYPOINT ["python", "-m", "prbr25_startgg_queries"]
