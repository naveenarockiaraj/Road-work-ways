"""The disposable-database guard must refuse anything that could be a real database."""
import pytest

from tests.disposable_db import (
    DisposableServer,
    UnsafeTestDatabaseError,
    assert_isolated_test_url,
)

SAFE = "postgresql://u:p@127.0.0.1:55432/postgres"


def test_accepts_loopback_server_on_isolated_port():
    url = assert_isolated_test_url(SAFE, ["postgresql://u:p@localhost:5432/roadworks_db"])
    assert (url.host, url.port) == ("127.0.0.1", 55432)


@pytest.mark.parametrize(
    "raw",
    [
        "postgresql://u:p@127.0.0.1:5432/postgres",  # live stack port
        "postgresql://u:p@localhost/postgres",  # implicit default port
        "postgresql://u:p@db.example.com:55432/postgres",  # not loopback
        "postgresql://u:p@postgres:55432/postgres",  # docker service name
        "postgresql://u:p@127.0.0.1:55432/postgres?port=5432",  # query overrides port
        "postgresql://u:p@127.0.0.1:55432/postgres?host=db.example.com",
        "postgresql://u:p@127.0.0.1:55432/postgres?service=live",
        "sqlite:///rww_test.db",
        "not a url",
    ],
)
def test_rejects_unsafe_urls(raw):
    with pytest.raises(UnsafeTestDatabaseError):
        assert_isolated_test_url(raw)


def test_rejects_same_server_as_application_database():
    with pytest.raises(UnsafeTestDatabaseError):
        assert_isolated_test_url(SAFE, ["postgresql://x:y@localhost:55432/roadworks_db"])


def test_only_prefixed_databases_can_be_targeted_or_dropped():
    server = DisposableServer(assert_isolated_test_url(SAFE))
    with pytest.raises(UnsafeTestDatabaseError):
        server.url_for("roadworks_db")
    with pytest.raises(UnsafeTestDatabaseError):
        server.drop_database("roadworks_db")
