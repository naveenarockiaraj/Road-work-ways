"""Initial Alembic baseline: upgrade, downgrade, re-upgrade and schema drift detection.

Runs only against a disposable PostgreSQL server (see tests/disposable_db.py). Databases
are built exclusively by roadworks-db/init.sql + Alembic; Base.metadata.create_all is
never used.
"""
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

from tests.disposable_db import run_alembic
from tests.schema_inventory import capture_catalog, catalog_diff, load_reference_catalog

pytestmark = pytest.mark.disposable_db

BASELINE_REVISION = "d2fa37494fac"
APPLICATION_TABLES = {
    "attendance",
    "employee_logs",
    "employees",
    "expenses",
    "material_stock",
    "material_transactions",
    "materials",
    "projects",
    "users",
    "vendors",
}
ENUM_TYPES = {
    "attendance_status_enum",
    "employee_status_enum",
    "expense_category_enum",
    "project_status_enum",
    "road_type_enum",
    "transaction_type_enum",
    "user_role_enum",
}


def _scalar_set(url: str, sql: str) -> set:
    engine = create_engine(url, poolclass=NullPool)
    try:
        with engine.connect() as connection:
            return {row[0] for row in connection.execute(text(sql))}
    finally:
        engine.dispose()


def _public_tables(url: str) -> set:
    return _scalar_set(url, "SELECT tablename FROM pg_tables WHERE schemaname = 'public'")


def _public_enums(url: str) -> set:
    return _scalar_set(
        url,
        "SELECT t.typname FROM pg_type t JOIN pg_namespace n ON n.oid = t.typnamespace "
        "WHERE n.nspname = 'public' AND t.typtype = 'e'",
    )


def _public_sequences(url: str) -> set:
    return _scalar_set(url, "SELECT sequencename FROM pg_sequences WHERE schemaname = 'public'")


def _alembic_ok(url: str, *args: str) -> str:
    result = run_alembic(url, *args)
    assert result.returncode == 0, f"alembic {' '.join(args)} failed:\n{result.stderr[-3000:]}"
    return result.stdout + result.stderr


def _assert_matches_reference(url: str) -> None:
    diff = catalog_diff(load_reference_catalog(), capture_catalog(url))
    assert not diff, "Schema differs from the Phase 1B-1 reference:\n" + "\n".join(diff)


def _section(lines: list, header_prefix: str) -> list:
    start = next(i for i, line in enumerate(lines) if line.startswith(header_prefix)) + 1
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    return lines[start:end]


def test_reference_catalog_fixture_is_complete():
    reference = load_reference_catalog()
    tables = {line.split(" | ")[0] for line in _section(reference, "## TABLES")}
    enums = {line.split(" | ")[0] for line in _section(reference, "## ENUMS")}
    sequences = _section(reference, "## SEQUENCES")
    assert tables == APPLICATION_TABLES | {"alembic_version"}
    assert enums == ENUM_TYPES
    assert len(sequences) == 10 and all(" | public." in line for line in sequences)


def test_upgrade_creates_reference_schema_on_empty_database(empty_db):
    assert _public_tables(empty_db) == set()

    _alembic_ok(empty_db, "upgrade", "head")

    assert _public_tables(empty_db) == APPLICATION_TABLES | {"alembic_version"}
    assert _public_enums(empty_db) == ENUM_TYPES
    assert len(_public_sequences(empty_db)) == 10
    assert BASELINE_REVISION in _alembic_ok(empty_db, "current")
    _assert_matches_reference(empty_db)


def test_alembic_check_reports_no_pending_changes(migrated_db):
    output = _alembic_ok(migrated_db, "check")
    assert "No new upgrade operations detected" in output


def test_repeated_upgrade_is_a_noop(migrated_db):
    output = _alembic_ok(migrated_db, "upgrade", "head")
    assert "Running upgrade" not in output
    _assert_matches_reference(migrated_db)


def test_downgrade_removes_all_application_objects(migrated_db):
    _alembic_ok(migrated_db, "downgrade", "base")

    assert _public_tables(migrated_db) == {"alembic_version"}
    assert _public_enums(migrated_db) == set()
    assert _public_sequences(migrated_db) == set()
    assert _scalar_set(migrated_db, "SELECT count(*) FROM alembic_version") == {0}
    # init.sql owns the extensions, so the migration leaves them in place.
    assert {"pg_trgm", "uuid-ossp"} <= _scalar_set(migrated_db, "SELECT extname FROM pg_extension")


def test_upgrade_after_downgrade_recreates_reference_schema(migrated_db):
    _alembic_ok(migrated_db, "downgrade", "base")
    _alembic_ok(migrated_db, "upgrade", "head")

    _assert_matches_reference(migrated_db)
    assert "No new upgrade operations detected" in _alembic_ok(migrated_db, "check")


def test_schema_comparison_detects_unexpected_changes(migrated_db):
    engine = create_engine(migrated_db, poolclass=NullPool, isolation_level="AUTOCOMMIT")
    try:
        with engine.connect() as connection:
            connection.execute(text("ALTER TABLE vendors ADD COLUMN unexpected_col integer"))
            connection.execute(text("CREATE INDEX ix_unexpected ON users (full_name)"))
            connection.execute(text("ALTER TYPE user_role_enum ADD VALUE 'UNEXPECTED_ROLE'"))
    finally:
        engine.dispose()

    diff = "\n".join(catalog_diff(load_reference_catalog(), capture_catalog(migrated_db)))
    assert "unexpected_col" in diff
    assert "ix_unexpected" in diff
    assert "UNEXPECTED_ROLE" in diff

    check = run_alembic(migrated_db, "check")
    assert check.returncode != 0
    assert "New upgrade operations detected" in check.stdout + check.stderr
