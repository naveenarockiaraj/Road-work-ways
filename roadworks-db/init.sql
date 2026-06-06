-- Road Work Ways — PostgreSQL initialization
-- Run once to enable extensions.
-- The database is created automatically via POSTGRES_DB env var.
-- Alembic migrations create the actual tables.

\c roadworks_db

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- optional: for fast text search
