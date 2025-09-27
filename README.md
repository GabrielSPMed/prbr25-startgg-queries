# prbr25-startgg-queries

## Overview

`prbr25-startgg-queries` is a Python project for extracting, transforming, and loading tournament and event data from the start.gg API into a PostgreSQL database. It uses GraphQL queries to fetch tournament information, processes the data, and stores it in database tables for further analysis.

## Features

- Fetches tournament and event data from start.gg using GraphQL
- Cleans and transforms event and phase data
- Loads data into PostgreSQL tables (`raw_events`, `raw_phases`)
- Supports Docker and Poetry for environment management
- IMPORTANT: As for now is intended for SMALL VOLUMES OF DATA as it uses pandas

## Usage

1. Install dependencies:
	```bash
	poetry install
	```
2. Set up your `.env` file with the required environment variables (see below).
3. Run the main entrypoint:
	```bash
	poetry run python -m prbr25_startgg_queries
	```
4. Optionally, use Docker:
	```bash
	docker build -t startgg-queries .
	docker run --env-file .env startgg-queries
	```

## Required .env Variables

The project requires a `.env` file in the root directory with the following variables:

| Variable               | Description                                                      |
|------------------------|------------------------------------------------------------------|
| STARTGG_BEARER_TOKEN   | Bearer token for authenticating with the start.gg API             |
| POSTGRES_USERNAME      | Username for the PostgreSQL database                              |
| POSTGRES_PASSWORD      | Password for the PostgreSQL database                              |
| POSTGRES_PORT          | Port for the PostgreSQL database (default: 5432)                  |
| POSTGRES_DB            | Name of the PostgreSQL database                                   |
| POSTGRES_HOST          | Hostname or endpoint for the PostgreSQL database                  |
| MAX_DATE_LIMIT         | Maximum timestamp for event queries (Unix timestamp, int)         |
| MIN_DATE_LIMIT         | Minimum timestamp for event queries (Unix timestamp, int)         |
| COUNTRY_CODE           | Country code for filtering tournaments (e.g., 'BR' for Brazil)    |
| STARTGG_VIDEOGAME_ID   | ID of the videogame to filter events (integer, e.g., 1386)        |

Example `.env` file:

```env
STARTGG_BEARER_TOKEN=your_startgg_token
POSTGRES_USERNAME=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_PORT=5432
POSTGRES_DB=your_db_name
POSTGRES_HOST=your_db_host
MAX_DATE_LIMIT=1764557999
MIN_DATE_LIMIT=1733022000
COUNTRY_CODE=BR
STARTGG_VIDEOGAME_ID=1386
```

## Project Structure

- `src/prbr25_startgg_queries/` - Main source code
- `src/prbr25_startgg_queries/extract/` - Data extraction logic
- `src/prbr25_startgg_queries/transform/` - Data transformation logic
- `src/prbr25_startgg_queries/bd/` - Database interaction
- `src/prbr25_startgg_queries/queries/` - GraphQL and SQL queries
- `pyproject.toml` - Poetry configuration
- `Dockerfile` - Docker setup
- `.env` - Environment variables

## License

MIT License
