"""Helpers for tests that need a real, disposable PostgreSQL server.

Database tests run only when ``RWW_TEST_DATABASE_URL`` names a maintenance database on a
disposable server, for example::

    RWW_TEST_DATABASE_URL=postgresql://rww_test:<pw>@127.0.0.1:55432/postgres

Every database the tests touch is created here with a ``rww_test_`` prefix and dropped
afterwards. ``assert_isolated_test_url`` refuses (and aborts the whole pytest run via
``conftest.pytest_configure``) any URL that is not a loopback, non-default-port server
distinct from the application's configured database.
"""
from __future__ import annotations

import os
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Iterable, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL, make_url
from sqlalchemy.pool import NullPool

API_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = API_ROOT.parent
INIT_SQL = REPO_ROOT / "roadworks-db" / "init.sql"

TEST_DB_ENV = "RWW_TEST_DATABASE_URL"
TEST_DB_PREFIX = "rww_test_"
LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}
# 5432 is the port the real stack publishes; a disposable server must use another one.
FORBIDDEN_PORTS = {5432}


class UnsafeTestDatabaseError(RuntimeError):
    pass


def _dotenv_database_url() -> Optional[str]:
    env_file = API_ROOT / ".env"
    if not env_file.is_file():
        return None
    for line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
        key, sep, value = line.partition("=")
        if sep and key.strip() == "DATABASE_URL":
            return value.strip().strip('"').strip("'")
    return None


def _server_key(url: URL) -> tuple[str, Optional[int]]:
    host = (url.host or "").lower()
    if host == "localhost":
        host = "127.0.0.1"
    return host, url.port or 5432


def assert_isolated_test_url(raw_url: str, protected_urls: Iterable[Optional[str]] = ()) -> URL:
    """Validate that ``raw_url`` points at an explicitly isolated disposable server."""
    try:
        url = make_url(raw_url)
    except Exception:
        raise UnsafeTestDatabaseError(f"{TEST_DB_ENV} is not a valid SQLAlchemy URL.") from None

    if not url.drivername.startswith("postgresql"):
        raise UnsafeTestDatabaseError(f"{TEST_DB_ENV} must be a PostgreSQL URL.")
    if url.query:
        # libpq/psycopg2 apply query options (port, host, hostaddr, service) after the
        # URL's host/port, which would bypass the checks below.
        raise UnsafeTestDatabaseError(f"{TEST_DB_ENV} must not contain query parameters.")
    if url.host not in LOOPBACK_HOSTS:
        raise UnsafeTestDatabaseError(f"{TEST_DB_ENV} must use a loopback host (127.0.0.1).")
    if url.port is None:
        raise UnsafeTestDatabaseError(f"{TEST_DB_ENV} must specify an explicit port.")
    if url.port in FORBIDDEN_PORTS:
        raise UnsafeTestDatabaseError(
            f"{TEST_DB_ENV} uses port {url.port}, which is reserved for the real stack."
        )
    for protected in protected_urls:
        if not protected:
            continue
        try:
            protected_url = make_url(protected)
        except Exception:
            continue
        if _server_key(protected_url) == _server_key(url):
            raise UnsafeTestDatabaseError(
                f"{TEST_DB_ENV} points at the same server as the application's DATABASE_URL."
            )
    return url


def protected_application_urls(original_env_url: Optional[str]) -> list[Optional[str]]:
    return [original_env_url, _dotenv_database_url()]


class DisposableServer:
    def __init__(self, maintenance_url: URL):
        self.maintenance_url = maintenance_url

    def url_for(self, database: str) -> str:
        if not database.startswith(TEST_DB_PREFIX):
            raise UnsafeTestDatabaseError("tests may only use databases prefixed with rww_test_.")
        return self.maintenance_url.set(database=database).render_as_string(hide_password=False)

    def _admin(self, sql: str) -> None:
        engine = create_engine(self.maintenance_url, poolclass=NullPool, isolation_level="AUTOCOMMIT")
        try:
            with engine.connect() as connection:
                connection.execute(text(sql))
        finally:
            engine.dispose()

    def create_database(self, template: Optional[str] = None) -> str:
        name = f"{TEST_DB_PREFIX}{uuid.uuid4().hex[:12]}"
        clause = f' TEMPLATE "{template}"' if template else ""
        self._admin(f'CREATE DATABASE "{name}"{clause}')
        return name

    def drop_database(self, name: str) -> None:
        if not name.startswith(TEST_DB_PREFIX):
            raise UnsafeTestDatabaseError("refusing to drop a database without the rww_test_ prefix.")
        self._admin(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)')

    def apply_init_sql(self, database: str) -> None:
        """Run roadworks-db/init.sql (extension ownership) minus psql meta-commands."""
        statements = "\n".join(
            line for line in INIT_SQL.read_text(encoding="utf-8").splitlines()
            if not line.lstrip().startswith("\\")
        )
        engine = create_engine(self.url_for(database), poolclass=NullPool, isolation_level="AUTOCOMMIT")
        try:
            with engine.connect() as connection:
                connection.exec_driver_sql(statements)
        finally:
            engine.dispose()


def subprocess_env(database_url: str) -> dict[str, str]:
    env = dict(os.environ)
    env["DATABASE_URL"] = database_url
    env.pop(TEST_DB_ENV, None)
    for key in ("ROADWORKS_ADMIN_USERNAME", "ROADWORKS_ADMIN_EMAIL", "ROADWORKS_ADMIN_FULL_NAME"):
        env.pop(key, None)
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def run_alembic(database_url: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "alembic", "-c", str(API_ROOT / "alembic.ini"), *args],
        cwd=API_ROOT,
        env=subprocess_env(database_url),
        capture_output=True,
        text=True,
        timeout=180,
    )
