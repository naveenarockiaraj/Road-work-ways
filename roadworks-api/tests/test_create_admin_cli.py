"""Explicit SUPER_ADMIN creation CLI (python -m app.cli.create_admin).

The command is exercised as a real subprocess against disposable databases only.
"""
import io
import secrets
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

from app.cli import create_admin
from app.core.security import get_password_hash, verify_password
from tests.disposable_db import API_ROOT, subprocess_env

ADMIN = {"username": "rootadmin", "email": "rootadmin@example.com", "full_name": "Root Admin"}


def _password() -> str:
    return "Pw-" + secrets.token_urlsafe(18)


def _run_cli(database_url: str, *args: str, stdin: str = "", identity: dict = ADMIN):
    argv = [sys.executable, "-m", "app.cli.create_admin"]
    if identity:
        argv += [
            "--username", identity["username"],
            "--email", identity["email"],
            "--full-name", identity["full_name"],
        ]
    argv += list(args)
    return subprocess.run(
        argv,
        cwd=API_ROOT,
        env=subprocess_env(database_url),
        input=stdin,
        capture_output=True,
        text=True,
        timeout=120,
    )


def _create(database_url: str, password: str, identity: dict = ADMIN):
    return _run_cli(database_url, "--password-stdin", stdin=password + "\n", identity=identity)


def _users(database_url: str) -> list[dict]:
    engine = create_engine(database_url, poolclass=NullPool)
    try:
        with engine.connect() as connection:
            rows = connection.execute(
                text(
                    "SELECT id, username, email, full_name, password_hash, role::text AS role, "
                    "is_active, created_at, updated_at FROM users ORDER BY id"
                )
            )
            return [dict(row._mapping) for row in rows]
    finally:
        engine.dispose()


def _execute(database_url: str, sql: str, **params) -> None:
    engine = create_engine(database_url, poolclass=NullPool)
    try:
        with engine.begin() as connection:
            connection.execute(text(sql), params)
    finally:
        engine.dispose()


def _insert_user(database_url: str, username: str, email: str, role: str, password: str) -> None:
    _execute(
        database_url,
        "INSERT INTO users (username, email, full_name, password_hash, role, is_active, created_at, updated_at) "
        "VALUES (:u, :e, 'Existing User', :h, CAST(:r AS user_role_enum), true, "
        "TIMESTAMP '2024-01-01 00:00:00', TIMESTAMP '2024-01-01 00:00:00')",
        u=username,
        e=email,
        h=get_password_hash(password),
        r=role,
    )


def _assert_no_secrets(result, password: str, database_url: str) -> None:
    output = result.stdout + result.stderr
    assert password not in output
    assert "$2b$" not in output
    for row in _users(database_url):
        assert row["password_hash"] not in output


# ---- Pure unit tests (no database) -------------------------------------------------------


def test_cli_has_no_password_argument():
    parser = create_admin._build_parser()
    options = {opt for action in parser._actions for opt in action.option_strings}
    assert not {o for o in options if "password" in o} - {"--password-stdin"}
    assert parser.allow_abbrev is False


@pytest.mark.parametrize(
    "argv_template",
    [
        ["--password", "{secret}"],
        ["--password={secret}"],
        ["--password-stdin={secret}"],
        ["--username", "admin", "{secret}"],
    ],
)
def test_password_argument_is_rejected_without_echo(capsys, argv_template):
    secret = _password()
    argv = [part.format(secret=secret) for part in argv_template]
    with pytest.raises(SystemExit) as excinfo:
        create_admin._build_parser().parse_args(argv)
    assert excinfo.value.code == 2
    captured = capsys.readouterr()
    assert secret not in captured.out + captured.err


def test_help_flag_with_attached_value_does_not_echo_it(capsys):
    secret = _password()
    with pytest.raises(SystemExit) as excinfo:
        create_admin._build_parser().parse_args([f"-h{secret}"])
    assert excinfo.value.code in (0, 2)
    captured = capsys.readouterr()
    assert secret not in captured.out + captured.err


def test_validation_errors_never_include_the_password():
    secret = "short1"
    with pytest.raises(create_admin.CliError) as excinfo:
        create_admin._validate("rootadmin", "rootadmin@example.com", "Root Admin", secret)
    assert excinfo.value.code == create_admin.ExitCode.INVALID_INPUT
    assert secret not in excinfo.value.message
    assert "password" in excinfo.value.message


def test_interactive_password_mismatch_is_rejected(monkeypatch):
    class FakeTty(io.StringIO):
        def isatty(self):
            return True

    answers = iter(["First-password-1", "Second-password-2"])
    monkeypatch.setattr(create_admin.getpass, "getpass", lambda prompt="": next(answers))
    with pytest.raises(create_admin.CliError) as excinfo:
        create_admin._read_password(False, FakeTty())
    assert excinfo.value.code == create_admin.ExitCode.INVALID_INPUT


def test_password_prompt_requires_a_terminal():
    with pytest.raises(create_admin.CliError) as excinfo:
        create_admin._read_password(False, io.StringIO("ignored\n"))
    assert excinfo.value.code == create_admin.ExitCode.INVALID_INPUT


def test_cli_is_never_invoked_by_application_startup():
    app_dir = API_ROOT / "app"
    offenders = [
        str(path.relative_to(API_ROOT))
        for path in app_dir.rglob("*.py")
        if path.parent.name != "cli" and "create_admin" in path.read_text(encoding="utf-8")
    ]
    assert offenders == []


# ---- Disposable database tests ------------------------------------------------------------


@pytest.mark.disposable_db
def test_creates_super_admin(migrated_db):
    password = _password()
    result = _create(migrated_db, password)

    assert result.returncode == 0, result.stderr
    assert "created" in result.stdout
    users = _users(migrated_db)
    assert len(users) == 1
    user = users[0]
    assert (user["username"], user["email"], user["full_name"]) == (
        ADMIN["username"], ADMIN["email"], ADMIN["full_name"],
    )
    assert user["role"] == "SUPER_ADMIN" and user["is_active"] is True
    assert verify_password(password, user["password_hash"])
    _assert_no_secrets(result, password, migrated_db)


@pytest.mark.disposable_db
def test_repeated_invocation_is_idempotent_and_changes_nothing(migrated_db):
    first_password = _password()
    assert _create(migrated_db, first_password).returncode == 0
    before = _users(migrated_db)

    second_password = _password()
    result = _create(migrated_db, second_password)

    assert result.returncode == 0, result.stderr
    assert "already" in result.stdout.lower()
    after = _users(migrated_db)
    assert after == before
    assert verify_password(first_password, after[0]["password_hash"])
    assert not verify_password(second_password, after[0]["password_hash"])
    _assert_no_secrets(result, second_password, migrated_db)


@pytest.mark.disposable_db
def test_refuses_when_a_different_super_admin_exists(migrated_db):
    _insert_user(migrated_db, "existing_admin", "existing@example.com", "SUPER_ADMIN", _password())
    before = _users(migrated_db)

    password = _password()
    result = _create(migrated_db, password)

    assert result.returncode == 4
    assert "different SUPER_ADMIN" in result.stderr
    assert _users(migrated_db) == before
    _assert_no_secrets(result, password, migrated_db)


@pytest.mark.disposable_db
def test_never_promotes_an_existing_account_with_the_same_username(migrated_db):
    existing_password = _password()
    _insert_user(migrated_db, ADMIN["username"], "someone@example.com", "SITE_ENGINEER", existing_password)
    before = _users(migrated_db)

    password = _password()
    result = _create(migrated_db, password)

    assert result.returncode == 4
    assert "never promoted" in result.stderr
    after = _users(migrated_db)
    assert after == before
    assert after[0]["role"] == "SITE_ENGINEER"
    assert verify_password(existing_password, after[0]["password_hash"])
    _assert_no_secrets(result, password, migrated_db)


@pytest.mark.disposable_db
@pytest.mark.parametrize(
    "existing_username, existing_email",
    [
        ("someone_else", ADMIN["email"]),
        ("someone_else", ADMIN["email"].upper()),
        (ADMIN["username"].upper(), "other@example.com"),
    ],
)
def test_refuses_username_or_email_owned_by_another_account(migrated_db, existing_username, existing_email):
    _insert_user(migrated_db, existing_username, existing_email, "ACCOUNTANT", _password())
    before = _users(migrated_db)

    password = _password()
    result = _create(migrated_db, password)

    assert result.returncode == 4
    assert _users(migrated_db) == before
    _assert_no_secrets(result, password, migrated_db)


@pytest.mark.disposable_db
def test_refuses_when_database_has_no_migrations(empty_db):
    password = _password()
    result = _create(empty_db, password)

    assert result.returncode == 3
    assert "not at the Alembic head" in result.stderr
    engine = create_engine(empty_db, poolclass=NullPool)
    try:
        with engine.connect() as connection:
            tables = connection.execute(
                text("SELECT count(*) FROM pg_tables WHERE schemaname = 'public'")
            ).scalar_one()
    finally:
        engine.dispose()
    assert tables == 0
    assert password not in result.stdout + result.stderr


@pytest.mark.disposable_db
def test_refuses_when_database_revision_is_not_head(migrated_db):
    _execute(migrated_db, "UPDATE alembic_version SET version_num = '000000000000'")

    password = _password()
    result = _create(migrated_db, password)

    assert result.returncode == 3
    assert "not at the Alembic head" in result.stderr
    assert _users(migrated_db) == []
    _assert_no_secrets(result, password, migrated_db)


@pytest.mark.disposable_db
def test_invalid_input_is_rejected_before_touching_the_database(migrated_db):
    weak = "short1"
    result = _create(migrated_db, weak)
    assert result.returncode == 2
    assert weak not in result.stdout + result.stderr

    bad_email = dict(ADMIN, email="not-an-email")
    result = _create(migrated_db, _password(), identity=bad_email)
    assert result.returncode == 2

    result = _run_cli(migrated_db, "--password-stdin", stdin="")
    assert result.returncode == 2
    assert _users(migrated_db) == []


@pytest.mark.disposable_db
def test_password_on_command_line_is_refused_and_not_echoed(migrated_db):
    secret = _password()
    result = _run_cli(migrated_db, "--password", secret)

    assert result.returncode == 2
    assert secret not in result.stdout + result.stderr
    assert _users(migrated_db) == []


@pytest.mark.disposable_db
def test_identity_can_come_from_environment_variables(migrated_db):
    password = _password()
    env = subprocess_env(migrated_db)
    env.update(
        ROADWORKS_ADMIN_USERNAME="envadmin",
        ROADWORKS_ADMIN_EMAIL="envadmin@example.com",
        ROADWORKS_ADMIN_FULL_NAME="Env Admin",
    )
    result = subprocess.run(
        [sys.executable, "-m", "app.cli.create_admin", "--password-stdin"],
        cwd=API_ROOT, env=env, input=password + "\n", capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0, result.stderr
    assert [u["username"] for u in _users(migrated_db)] == ["envadmin"]
    _assert_no_secrets(result, password, migrated_db)


@pytest.mark.disposable_db
def test_concurrent_invocations_create_exactly_one_admin(migrated_db):
    identities = [
        {"username": f"racer{i}", "email": f"racer{i}@example.com", "full_name": f"Racer {i}"}
        for i in range(2)
    ]
    passwords = [_password() for _ in identities]
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda pair: _create(migrated_db, pair[1], pair[0]), zip(identities, passwords)))

    assert sorted(r.returncode for r in results) == [0, 4], [r.stderr for r in results]
    admins = [u for u in _users(migrated_db) if u["role"] == "SUPER_ADMIN"]
    assert len(admins) == 1
    for result, password in zip(results, passwords):
        _assert_no_secrets(result, password, migrated_db)


@pytest.mark.disposable_db
def test_concurrent_identical_invocations_are_idempotent(migrated_db):
    passwords = [_password(), _password()]
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda pw: _create(migrated_db, pw), passwords))

    assert [r.returncode for r in results] == [0, 0], [r.stderr for r in results]
    assert sum("created" in r.stdout for r in results) == 1
    assert sum("already" in r.stdout.lower() for r in results) == 1
    assert len(_users(migrated_db)) == 1
