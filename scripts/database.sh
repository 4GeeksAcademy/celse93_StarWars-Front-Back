#!/usr/bin/env bash
set -e

# Load environment variables from .env
export $(grep -v '^#' .env | xargs)

# Remove migrations folder
rm -rf ./migrations

# Drop + recreate the database
PGPASSWORD=postgres dropdb -h localhost -U gitpod example || true
PGPASSWORD=postgres createdb -h localhost -U gitpod example

# Ensure useful extensions exist
psql "$DATABASE_URL" -c 'CREATE EXTENSION IF NOT EXISTS unaccent;' || true

# Re-initialize Alembic migrations
pipenv run init
pipenv run migrate
pipenv run upgrade
