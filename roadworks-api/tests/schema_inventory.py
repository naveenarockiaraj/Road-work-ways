"""Catalog inventory used to compare an Alembic-built schema with the Phase 1B-1 reference.

The queries and output format mirror the read-only ``catalog.sql`` that produced
``schema_reference/phase1b1_live_catalog.txt`` from the live database (psql unaligned
output, `` | `` separator, booleans as ``t``/``f``), so the reference can be compared
line by line without regeneration.
"""
from __future__ import annotations

import difflib
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

REFERENCE_CATALOG = Path(__file__).parent / "schema_reference" / "phase1b1_live_catalog.txt"

SECTIONS: list[tuple[str, str]] = [
    (
        "## TABLES",
        """SELECT c.relname, c.relkind FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
        WHERE n.nspname='public' AND c.relkind IN ('r','p','v','m','f') ORDER BY 1""",
    ),
    (
        "## COLUMNS (table | ordinal | column | type | notnull | default | identity)",
        """SELECT c.relname, a.attnum, a.attname, format_type(a.atttypid, a.atttypmod), a.attnotnull,
               coalesce(pg_get_expr(d.adbin, d.adrelid), '-'), coalesce(nullif(a.attidentity,''),'-')
        FROM pg_attribute a JOIN pg_class c ON c.oid=a.attrelid JOIN pg_namespace n ON n.oid=c.relnamespace
        LEFT JOIN pg_attrdef d ON d.adrelid=a.attrelid AND d.adnum=a.attnum
        WHERE n.nspname='public' AND c.relkind='r' AND a.attnum>0 AND NOT a.attisdropped ORDER BY 1,2""",
    ),
    (
        "## CONSTRAINTS (table | name | type | definition)",
        """SELECT conrelid::regclass::text, conname, contype, pg_get_constraintdef(oid)
        FROM pg_constraint WHERE connamespace='public'::regnamespace ORDER BY 1,2""",
    ),
    (
        "## INDEXES (table | name | definition)",
        """SELECT tablename, indexname, indexdef FROM pg_indexes WHERE schemaname='public' ORDER BY 1,2""",
    ),
    (
        "## ENUMS (type | sortorder | label)",
        """SELECT t.typname, e.enumsortorder, e.enumlabel FROM pg_type t JOIN pg_enum e ON e.enumtypid=t.oid
        JOIN pg_namespace n ON n.oid=t.typnamespace WHERE n.nspname='public' ORDER BY 1,2""",
    ),
    (
        "## OTHER TYPES (non-enum, user-defined, excluding table rowtypes/arrays)",
        """SELECT t.typname, t.typtype FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace
        WHERE n.nspname='public' AND t.typtype NOT IN ('e','c') AND t.typelem=0 ORDER BY 1""",
    ),
    (
        "## SEQUENCES (name | type | start | increment | owned_by)",
        """SELECT s.sequencename, s.data_type, s.start_value, s.increment_by,
               coalesce((SELECT d.refobjid::regclass::text || '.' || a.attname FROM pg_depend d
                         JOIN pg_attribute a ON a.attrelid=d.refobjid AND a.attnum=d.refobjsubid
                         WHERE d.objid=(quote_ident(s.schemaname)||'.'||quote_ident(s.sequencename))::regclass
                           AND d.deptype IN ('a','i') LIMIT 1), '-')
        FROM pg_sequences s WHERE s.schemaname='public' ORDER BY 1""",
    ),
    (
        "## EXTENSIONS (name | version | schema)",
        """SELECT e.extname, e.extversion, n.nspname FROM pg_extension e
        JOIN pg_namespace n ON n.oid=e.extnamespace ORDER BY 1""",
    ),
    (
        "## VIEWS / MATVIEWS",
        """SELECT schemaname, viewname FROM pg_views WHERE schemaname NOT IN ('pg_catalog','information_schema')
        UNION ALL SELECT schemaname, matviewname FROM pg_matviews ORDER BY 1,2""",
    ),
    (
        "## USER TRIGGERS",
        """SELECT tgrelid::regclass::text, tgname FROM pg_trigger WHERE NOT tgisinternal ORDER BY 1,2""",
    ),
    (
        "## USER FUNCTIONS IN public (excluding extension members)",
        """SELECT p.proname, pg_get_function_identity_arguments(p.oid) FROM pg_proc p
        JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='public'
        AND NOT EXISTS (SELECT 1 FROM pg_depend d WHERE d.objid=p.oid AND d.deptype='e') ORDER BY 1,2""",
    ),
    (
        "## NON-public SCHEMAS",
        """SELECT nspname FROM pg_namespace WHERE nspname NOT IN ('public','information_schema')
        AND nspname NOT LIKE 'pg\\_%' ORDER BY 1""",
    ),
]


def _psql_format(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "t" if value else "f"
    if isinstance(value, float):
        # psql renders float4 (e.g. pg_enum.enumsortorder) in shortest form: 1, 1.5
        return format(value, "g")
    return str(value)


def capture_catalog(database_url: str) -> list[str]:
    """Return the catalog inventory lines for ``database_url`` using a read-only transaction."""
    engine = create_engine(database_url, poolclass=NullPool)
    try:
        with engine.connect() as connection, connection.begin():
            connection.execute(text("SET TRANSACTION READ ONLY"))
            # Same search_path as catalog.sql so regclass/defaults render schema-qualified.
            connection.execute(text("SET LOCAL search_path = pg_catalog"))
            lines: list[str] = []
            for header, query in SECTIONS:
                lines.append(header)
                for row in connection.execute(text(query)):
                    lines.append(" | ".join(_psql_format(v) for v in row))
            return lines
    finally:
        engine.dispose()


def load_reference_catalog() -> list[str]:
    return REFERENCE_CATALOG.read_text(encoding="utf-8").splitlines()


def catalog_diff(expected: list[str], actual: list[str]) -> list[str]:
    return list(
        difflib.unified_diff(expected, actual, "phase1b1_reference", "actual", lineterm="", n=0)
    )
