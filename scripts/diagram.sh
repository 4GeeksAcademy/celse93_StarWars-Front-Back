#!/usr/bin/env bash
set -e

# Load environment variables
export $(grep -v '^#' .env | xargs)

eralchemy2 -i "$DATABASE_URL" -o diagram.png
