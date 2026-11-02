import os

# Captured before the override below so the disposable-DB guard can refuse any test URL
# that points at the same server as the application's real configuration.
_ORIGINAL_DATABASE_URL = os.environ.get("DATABASE_URL")

# Must run before any `app` import: app.core.config instantiates Settings at import time.
# Real environment variables take precedence over values in roadworks-api/.env, so tests
# never receive a real database URL or secret. Port 1 on loopback refuses connections, so
# any accidental database access fails fast instead of reaching an existing database.
TEST_DATABASE_URL = "postgresql://rww_test:rww_test@127.0.0.1:1/rww_test_unreachable"

os.environ["DATABASE_URL"] = TEST_DATABASE_URL
os.environ["SECRET_KEY"] = "test-only-secret-key-not-used-outside-pytest-0123456789"

import pytest  # noqa: E402

from tests.disposable_db import (  # noqa: E402
    TEST_DB_ENV,
    DisposableServer,
    UnsafeTestDatabaseError,
    assert_isolated_test_url,
    protected_application_urls,
    run_alembic,
)

_DISPOSABLE_URL = None


def pytest_configure(config):
    global _DISPOSABLE_URL
    config.addinivalue_line(
        "markers", "disposable_db: needs a disposable PostgreSQL server via RWW_TEST_DATABASE_URL"
    )
    raw = os.environ.get(TEST_DB_ENV)
    if not raw:
        return
    try:
        _DISPOSABLE_URL = assert_isolated_test_url(
            raw, protected_application_urls(_ORIGINAL_DATABASE_URL)
        )
    except UnsafeTestDatabaseError as exc:
        # Abort the entire run before any test can connect anywhere.
        raise pytest.UsageError(f"Unsafe test database configuration: {exc}") from None


@pytest.fixture(scope="session")
def disposable_server():
    if _DISPOSABLE_URL is None:
        pytest.skip(f"{TEST_DB_ENV} is not set; disposable database tests skipped.")
    return DisposableServer(_DISPOSABLE_URL)


@pytest.fixture(scope="session")
def head_template_db(disposable_server):
    """A database built only by init.sql + `alembic upgrade head`, used as a CREATE DATABASE template."""
    name = disposable_server.create_database()
    try:
        disposable_server.apply_init_sql(name)
        result = run_alembic(disposable_server.url_for(name), "upgrade", "head")
        assert result.returncode == 0, result.stderr[-2000:]
        yield name
    finally:
        disposable_server.drop_database(name)


@pytest.fixture
def empty_db(disposable_server):
    """Fresh database with only the init.sql extensions (no Alembic, no create_all)."""
    name = disposable_server.create_database()
    try:
        disposable_server.apply_init_sql(name)
        yield disposable_server.url_for(name)
    finally:
        disposable_server.drop_database(name)


@pytest.fixture
def migrated_db(disposable_server, head_template_db):
    """Fresh database cloned from the Alembic-head template."""
    name = disposable_server.create_database(template=head_template_db)
    try:
        yield disposable_server.url_for(name)
    finally:
        disposable_server.drop_database(name)
