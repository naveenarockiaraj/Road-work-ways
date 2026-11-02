"""Smoke tests for application import and route registration.

None of these tests touch a database: settings point at an unreachable loopback port, and
application startup (the lifespan) no longer creates or alters the schema.
"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app
from tests.conftest import TEST_DATABASE_URL

EXPECTED_API_ROUTES = {
    ("POST", "/api/v1/auth/login"),
    ("POST", "/api/v1/auth/logout"),
    ("GET", "/api/v1/auth/me"),
    ("GET", "/api/v1/employees"),
    ("POST", "/api/v1/employees"),
    ("GET", "/api/v1/employees/{employee_id}"),
    ("PUT", "/api/v1/employees/{employee_id}"),
    ("DELETE", "/api/v1/employees/{employee_id}"),
    ("GET", "/api/v1/attendance"),
    ("POST", "/api/v1/attendance"),
    ("PUT", "/api/v1/attendance/{attendance_id}"),
    ("GET", "/api/v1/projects"),
    ("POST", "/api/v1/projects"),
    ("GET", "/api/v1/projects/{project_id}"),
    ("PUT", "/api/v1/projects/{project_id}"),
    ("DELETE", "/api/v1/projects/{project_id}"),
    ("GET", "/api/v1/materials"),
    ("POST", "/api/v1/materials"),
    ("GET", "/api/v1/materials/{material_id}"),
    ("PUT", "/api/v1/materials/{material_id}"),
    ("DELETE", "/api/v1/materials/{material_id}"),
    ("GET", "/api/v1/stock/project/{project_id}"),
    ("GET", "/api/v1/stock/low-stock"),
    ("POST", "/api/v1/stock/transaction"),
    ("GET", "/api/v1/vendors"),
    ("POST", "/api/v1/vendors"),
    ("GET", "/api/v1/vendors/{vendor_id}"),
    ("PUT", "/api/v1/vendors/{vendor_id}"),
    ("DELETE", "/api/v1/vendors/{vendor_id}"),
    ("GET", "/api/v1/expenses"),
    ("POST", "/api/v1/expenses"),
    ("GET", "/api/v1/expenses/{expense_id}"),
    ("PUT", "/api/v1/expenses/{expense_id}"),
    ("DELETE", "/api/v1/expenses/{expense_id}"),
    ("GET", "/api/v1/reports/dashboard"),
    ("GET", "/api/v1/reports/daily"),
    ("GET", "/api/v1/reports/monthly"),
    ("GET", "/api/v1/reports/material-consumption"),
    ("GET", "/health"),
}


def _registered_routes() -> set[tuple[str, str]]:
    routes = set()
    for route in app.routes:
        for method in getattr(route, "methods", None) or ():
            if method != "HEAD":
                routes.add((method, route.path))
    return routes


def test_tests_are_isolated_from_real_database():
    assert settings.DATABASE_URL == TEST_DATABASE_URL


def test_app_is_fastapi_instance_with_configured_docs():
    assert isinstance(app, FastAPI)
    assert app.title == settings.PROJECT_NAME
    assert app.docs_url == "/api/docs"
    assert app.openapi_url == "/api/openapi.json"


def test_all_expected_api_routes_are_registered():
    registered = _registered_routes()
    missing = EXPECTED_API_ROUTES - registered
    assert not missing, f"Missing routes: {sorted(missing)}"


def test_no_unexpected_api_routes_are_registered():
    registered_api = {r for r in _registered_routes() if r[1].startswith("/api/v1/")}
    unexpected = registered_api - EXPECTED_API_ROUTES
    assert not unexpected, f"Unexpected routes: {sorted(unexpected)}"


def test_openapi_schema_generates_for_all_api_routes():
    schema = app.openapi()
    documented = {
        (method.upper(), path)
        for path, operations in schema["paths"].items()
        for method in operations
    }
    assert EXPECTED_API_ROUTES - {("GET", "/health")} <= documented


def test_health_endpoint_responds_without_database():
    # Not using `with TestClient(app)` keeps the lifespan from running.
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert body["service"] == settings.PROJECT_NAME


def test_protected_route_rejects_request_without_bearer_token():
    client = TestClient(app)
    response = client.get("/api/v1/employees")
    # FastAPI 0.104 HTTPBearer(auto_error=True) rejects a missing Authorization header with 403.
    assert response.status_code == 403


def test_startup_lifespan_does_not_touch_the_database():
    # The configured database is unreachable, so any schema work at startup would fail here.
    with TestClient(app) as client:
        assert client.get("/health").status_code == 200


def test_no_automatic_schema_creation_or_admin_seeding_in_application_code():
    app_dir = Path(__file__).resolve().parents[1] / "app"
    offenders = []
    for path in app_dir.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        for marker in ("create_all(", "FIRST_SUPERUSER", "init_db("):
            if marker in source:
                offenders.append(f"{path.relative_to(app_dir)}: {marker}")
    assert offenders == []
