#!/usr/bin/env bash
set -e

export PGPASSWORD=postgres
DB_NAME="example"
DB_USER="gitpod"
PGHOST="localhost"


psql -h $PGHOST -U $DB_USER -d postgres -c "
  SELECT pg_terminate_backend(pid)
  FROM pg_stat_activity
  WHERE datname='$DB_NAME' AND pid <> pg_backend_pid();
" || true

dropdb -h $PGHOST -U $DB_USER $DB_NAME || true
createdb -h $PGHOST -U $DB_USER $DB_NAME || true
psql -h $PGHOST -U $DB_USER -d $DB_NAME -c "CREATE EXTENSION IF NOT EXISTS unaccent;" || true

rm -rf migrations || true

pipenv run flask db init || true
pipenv run flask db migrate -m "initial" || true
pipenv run flask db upgrade || true
