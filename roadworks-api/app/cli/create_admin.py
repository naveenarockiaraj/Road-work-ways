"""Create the first SUPER_ADMIN account explicitly and exactly once.

Usage (from the roadworks-api directory, with DATABASE_URL pointing at the target DB):

    python -m app.cli.create_admin --username admin --email admin@example.com \
        --full-name "System Administrator"
    printf '%s\n' "$PASSWORD" | python -m app.cli.create_admin ... --password-stdin

Identity values may also come from ROADWORKS_ADMIN_USERNAME, ROADWORKS_ADMIN_EMAIL and
ROADWORKS_ADMIN_FULL_NAME, or be typed interactively. The password is only ever read
from an interactive getpass prompt or from standard input (--password-stdin); it is
never accepted as a command-line argument or environment variable and is never printed.

The command never promotes, modifies or re-passwords an existing account. It refuses
to run unless the database is at the Alembic head revision. See EXIT_CODES below.
"""
from __future__ import annotations

import argparse
import getpass
import os
import sys
from datetime import datetime, timezone
from enum import IntEnum
from pathlib import Path
from typing import Optional, Sequence, TextIO

from pydantic import ValidationError
from sqlalchemy import create_engine, func, insert, or_, select, text
from sqlalchemy.engine import Connection, make_url
from sqlalchemy.exc import DBAPIError, IntegrityError, SQLAlchemyError
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.core.permissions import Role
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate

API_ROOT = Path(__file__).resolve().parents[2]

ENV_USERNAME = "ROADWORKS_ADMIN_USERNAME"
ENV_EMAIL = "ROADWORKS_ADMIN_EMAIL"
ENV_FULL_NAME = "ROADWORKS_ADMIN_FULL_NAME"

# Transaction-scoped advisory lock key shared by every create_admin invocation ("RWWADMIN").
ADVISORY_LOCK_KEY = 0x5257_5741_444D_494E
LOCK_TIMEOUT_SECONDS = 30
BCRYPT_MAX_PASSWORD_BYTES = 72
PG_LOCK_NOT_AVAILABLE = "55P03"


class ExitCode(IntEnum):
    CREATED = 0
    ALREADY_INITIALIZED = 0
    UNEXPECTED_ERROR = 1
    INVALID_INPUT = 2
    DATABASE_NOT_READY = 3
    CONFLICT = 4
    LOCK_TIMEOUT = 5
    INTERRUPTED = 130


EXIT_CODES = {
    0: "Administrator created, or the same username is already the SUPER_ADMIN (no changes).",
    1: "Unexpected error; the transaction was rolled back.",
    2: "Invalid or missing input (usage, validation, password entry).",
    3: "Database unreachable, or not at the Alembic head revision.",
    4: "Conflict: another SUPER_ADMIN exists, or the username/email belongs to another account.",
    5: "Another create_admin run held the initialization lock for too long.",
    130: "Interrupted by the operator; nothing was committed.",
}


class CliError(Exception):
    def __init__(self, code: ExitCode, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


class _SafeArgumentParser(argparse.ArgumentParser):
    """Never echo argparse's message: it can quote rejected values, e.g. a mistyped password."""

    def error(self, message: str) -> None:  # type: ignore[override]
        self.print_usage(sys.stderr)
        sys.stderr.write(
            f"{self.prog}: error: invalid arguments (details hidden so no value is echoed).\n"
            "Passwords are never accepted as arguments; use the interactive prompt or "
            "--password-stdin.\n"
        )
        raise SystemExit(int(ExitCode.INVALID_INPUT))


def _build_parser() -> argparse.ArgumentParser:
    epilog = "Exit codes:\n" + "\n".join(f"  {k:>3}  {v}" for k, v in EXIT_CODES.items())
    parser = _SafeArgumentParser(
        prog="python -m app.cli.create_admin",
        description="Create the first SUPER_ADMIN account (one-time, explicit).",
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        allow_abbrev=False,
    )
    parser.add_argument("--username", help=f"Admin username (or ${ENV_USERNAME}).")
    parser.add_argument("--email", help=f"Admin email (or ${ENV_EMAIL}).")
    parser.add_argument("--full-name", dest="full_name", help=f"Admin full name (or ${ENV_FULL_NAME}).")
    parser.add_argument(
        "--password-stdin",
        action="store_true",
        help="Read the password from the first line of standard input instead of prompting.",
    )
    return parser


def _out(message: str) -> None:
    print(message, file=sys.stdout, flush=True)


def _err(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr, flush=True)


def _resolve_value(
    cli_value: Optional[str], env_name: str, prompt: str, interactive: bool
) -> str:
    value = cli_value if cli_value is not None else os.environ.get(env_name)
    if value is None and interactive:
        value = input(prompt)
    if value is None or not value.strip():
        raise CliError(
            ExitCode.INVALID_INPUT,
            f"missing value for {prompt.rstrip(': ').lower()} (use the option or ${env_name}).",
        )
    return value.strip()


def _read_password(from_stdin: bool, stdin: TextIO) -> str:
    if from_stdin:
        line = stdin.readline()
        password = line.rstrip("\r\n")
        if not password:
            raise CliError(ExitCode.INVALID_INPUT, "no password received on standard input.")
        return password

    if not stdin.isatty():
        raise CliError(
            ExitCode.INVALID_INPUT,
            "no interactive terminal for the password prompt; use --password-stdin.",
        )
    password = getpass.getpass("Password: ")
    confirmation = getpass.getpass("Confirm password: ")
    if password != confirmation:
        raise CliError(ExitCode.INVALID_INPUT, "passwords do not match.")
    return password


def _validate(username: str, email: str, full_name: str, password: str) -> UserCreate:
    try:
        payload = UserCreate(
            username=username,
            email=email,
            full_name=full_name,
            password=password,
            role=Role.SUPER_ADMIN,
        )
    except ValidationError as exc:
        # Only field names and rule messages; never the rejected input values.
        details = "; ".join(
            f"{'.'.join(str(p) for p in error['loc'])}: {error['msg']}" for error in exc.errors()
        )
        raise CliError(ExitCode.INVALID_INPUT, f"invalid input: {details}") from None

    if len(password.encode("utf-8")) > BCRYPT_MAX_PASSWORD_BYTES:
        raise CliError(
            ExitCode.INVALID_INPUT,
            f"password must be at most {BCRYPT_MAX_PASSWORD_BYTES} bytes (bcrypt limit).",
        )
    return payload


def expected_alembic_heads() -> set[str]:
    from alembic.config import Config
    from alembic.script import ScriptDirectory

    config = Config(str(API_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(API_ROOT / "alembic"))
    return set(ScriptDirectory.from_config(config).get_heads())


def current_alembic_heads(connection: Connection) -> set[str]:
    from alembic.runtime.migration import MigrationContext

    return set(MigrationContext.configure(connection).get_current_heads())


def _describe_target(url: str) -> str:
    parsed = make_url(url)
    return f"{parsed.host or 'local socket'}:{parsed.port or 'default'}/{parsed.database}"


def _create_in_transaction(connection: Connection, payload: UserCreate, password_hash: str) -> str:
    expected = expected_alembic_heads()
    current = current_alembic_heads(connection)
    if not expected or current != expected:
        raise CliError(
            ExitCode.DATABASE_NOT_READY,
            "database is not at the Alembic head revision "
            f"(current: {', '.join(sorted(current)) or 'none'}; "
            f"expected: {', '.join(sorted(expected)) or 'none'}). "
            "Run migrations first; no changes were made.",
        )

    connection.execute(text(f"SET LOCAL lock_timeout = '{LOCK_TIMEOUT_SECONDS}s'"))
    # Serializes concurrent invocations; released automatically at commit/rollback.
    connection.execute(select(func.pg_advisory_xact_lock(ADVISORY_LOCK_KEY)))

    users = User.__table__
    same_username = connection.execute(
        select(users.c.id, users.c.role, users.c.is_active).where(users.c.username == payload.username)
    ).first()
    if same_username is not None:
        if same_username.role == Role.SUPER_ADMIN:
            note = "" if same_username.is_active else " (note: that account is inactive)"
            return (
                f"Initialization already completed: '{payload.username}' is already the "
                f"SUPER_ADMIN{note}. No changes were made."
            )
        raise CliError(
            ExitCode.CONFLICT,
            f"username '{payload.username}' belongs to an existing non-admin account. "
            "Existing accounts are never promoted. No changes were made.",
        )

    other_admin = connection.execute(
        select(users.c.id).where(users.c.role == Role.SUPER_ADMIN).limit(1)
    ).first()
    if other_admin is not None:
        raise CliError(
            ExitCode.CONFLICT,
            "a different SUPER_ADMIN account already exists. No changes were made.",
        )

    clash = connection.execute(
        select(users.c.id).where(
            or_(
                func.lower(users.c.username) == payload.username.lower(),
                func.lower(users.c.email) == payload.email.lower(),
            )
        ).limit(1)
    ).first()
    if clash is not None:
        raise CliError(
            ExitCode.CONFLICT,
            "the requested username or email is already used by another account. "
            "No changes were made.",
        )

    # Naive UTC, matching the models' existing datetime.utcnow defaults.
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    connection.execute(
        insert(users).values(
            username=payload.username,
            email=payload.email,
            full_name=payload.full_name,
            password_hash=password_hash,
            role=Role.SUPER_ADMIN,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
    )
    return f"SUPER_ADMIN '{payload.username}' created."


def run(argv: Optional[Sequence[str]] = None, stdin: Optional[TextIO] = None) -> int:
    stdin = stdin if stdin is not None else sys.stdin
    args = _build_parser().parse_args(argv)
    interactive = (not args.password_stdin) and stdin.isatty()

    username = _resolve_value(args.username, ENV_USERNAME, "Username: ", interactive)
    email = _resolve_value(args.email, ENV_EMAIL, "Email: ", interactive)
    full_name = _resolve_value(args.full_name, ENV_FULL_NAME, "Full name: ", interactive)
    password = _read_password(args.password_stdin, stdin)
    payload = _validate(username, email, full_name, password)

    # Hash before taking the lock so the critical section stays short.
    password_hash = get_password_hash(payload.password)
    del password

    _out(f"Target database: {_describe_target(settings.DATABASE_URL)}")
    engine = create_engine(settings.DATABASE_URL, poolclass=NullPool)
    try:
        try:
            connection = engine.connect()
        except DBAPIError:
            raise CliError(
                ExitCode.DATABASE_NOT_READY, "could not connect to the database. No changes were made."
            ) from None

        with connection:
            try:
                with connection.begin():
                    message = _create_in_transaction(connection, payload, password_hash)
            except IntegrityError:
                raise CliError(
                    ExitCode.CONFLICT,
                    "the username or email was taken concurrently. No changes were made.",
                ) from None
            except DBAPIError as exc:
                if getattr(exc.orig, "pgcode", None) == PG_LOCK_NOT_AVAILABLE:
                    raise CliError(
                        ExitCode.LOCK_TIMEOUT,
                        "another create_admin run is in progress; retry later. No changes were made.",
                    ) from None
                raise
    finally:
        engine.dispose()

    _out(message)
    return int(ExitCode.CREATED)


def main(argv: Optional[Sequence[str]] = None) -> int:
    try:
        return run(argv)
    except CliError as exc:
        _err(exc.message)
        return int(exc.code)
    except KeyboardInterrupt:
        _err("interrupted; no changes were committed.")
        return int(ExitCode.INTERRUPTED)
    except SQLAlchemyError as exc:
        # Exception text may contain SQL parameters (including the hash), so only the type is shown.
        _err(f"database error ({type(exc).__name__}); the transaction was rolled back.")
        return int(ExitCode.UNEXPECTED_ERROR)


if __name__ == "__main__":
    sys.exit(main())
