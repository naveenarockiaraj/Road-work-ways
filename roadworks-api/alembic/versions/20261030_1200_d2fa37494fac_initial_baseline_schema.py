"""initial baseline schema

Reproduces the schema verified in Phase 1B-1 (ten tables, seven enum types, ten
owned SERIAL sequences) with the exact PostgreSQL constraint and index names
that SQLAlchemy ``create_all()`` originally produced.

Extensions ``pg_trgm`` and ``uuid-ossp`` are intentionally NOT managed here; they
are owned by ``roadworks-db/init.sql`` and no table depends on them.

Revision ID: d2fa37494fac
Revises:
Create Date: 2026-10-30 12:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "d2fa37494fac"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Label order is significant for PostgreSQL enums and must match the live schema.
ENUMS = {
    "attendance_status_enum": ("PRESENT", "ABSENT", "HALF_DAY", "LEAVE", "HOLIDAY"),
    "employee_status_enum": ("ACTIVE", "INACTIVE", "TERMINATED"),
    "expense_category_enum": (
        "LABOUR",
        "MATERIAL",
        "EQUIPMENT",
        "FUEL",
        "TRANSPORT",
        "MISCELLANEOUS",
        "SUBCONTRACTOR",
        "SITE_EXPENSES",
    ),
    "project_status_enum": ("PLANNING", "IN_PROGRESS", "ON_HOLD", "COMPLETED", "CANCELLED"),
    "road_type_enum": (
        "NATIONAL_HIGHWAY",
        "STATE_HIGHWAY",
        "DISTRICT_ROAD",
        "RURAL_ROAD",
        "URBAN_ROAD",
        "OTHER",
    ),
    "transaction_type_enum": ("INWARD", "OUTWARD", "RETURN", "ADJUSTMENT"),
    "user_role_enum": (
        "SUPER_ADMIN",
        "CONTRACTOR",
        "PROJECT_MANAGER",
        "SITE_ENGINEER",
        "SITE_SUPERVISOR",
        "STORE_KEEPER",
        "ACCOUNTANT",
    ),
}

# Child tables first, so this order is safe for dropping.
TABLES_DROP_ORDER = (
    "material_transactions",
    "material_stock",
    "expenses",
    "employee_logs",
    "attendance",
    "vendors",
    "users",
    "materials",
    "projects",
    "employees",
)


def _enum(name: str) -> postgresql.ENUM:
    return postgresql.ENUM(*ENUMS[name], name=name, create_type=False)


def upgrade() -> None:
    bind = op.get_bind()
    for name, labels in ENUMS.items():
        postgresql.ENUM(*labels, name=name).create(bind, checkfirst=False)

    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("employee_code", sa.String(length=20), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("mobile_number", sa.String(length=15), nullable=False),
        sa.Column("aadhaar_number", sa.String(length=12), nullable=True),
        sa.Column("designation", sa.String(length=100), nullable=False),
        sa.Column("daily_wage", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("address", sa.String(length=500), nullable=True),
        sa.Column("joining_date", sa.Date(), nullable=False),
        sa.Column("status", _enum("employee_status_enum"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="employees_pkey"),
        sa.UniqueConstraint("aadhaar_number", name="employees_aadhaar_number_key"),
    )
    op.create_index("ix_employees_employee_code", "employees", ["employee_code"], unique=True)
    op.create_index("ix_employees_id", "employees", ["id"], unique=False)

    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_code", sa.String(length=30), nullable=False),
        sa.Column("project_name", sa.String(length=500), nullable=False),
        sa.Column("road_type", _enum("road_type_enum"), nullable=False),
        sa.Column("location", sa.String(length=500), nullable=True),
        sa.Column("district", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=100), nullable=False),
        sa.Column("contract_value", sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("status", _enum("project_status_enum"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="projects_pkey"),
    )
    op.create_index("ix_projects_id", "projects", ["id"], unique=False)
    op.create_index("ix_projects_project_code", "projects", ["project_code"], unique=True)

    op.create_table(
        "materials",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("material_code", sa.String(length=30), nullable=False),
        sa.Column("material_name", sa.String(length=255), nullable=False),
        sa.Column("unit", sa.String(length=30), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="materials_pkey"),
    )
    op.create_index("ix_materials_id", "materials", ["id"], unique=False)
    op.create_index("ix_materials_material_code", "materials", ["material_code"], unique=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", _enum("user_role_enum"), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="users_pkey"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    op.create_table(
        "vendors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("vendor_name", sa.String(length=255), nullable=False),
        sa.Column("contact_person", sa.String(length=255), nullable=True),
        sa.Column("mobile_number", sa.String(length=15), nullable=True),
        sa.Column("gst_number", sa.String(length=20), nullable=True),
        sa.Column("address", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="vendors_pkey"),
        sa.UniqueConstraint("gst_number", name="vendors_gst_number_key"),
    )
    op.create_index("ix_vendors_id", "vendors", ["id"], unique=False)
    op.create_index("ix_vendors_vendor_name", "vendors", ["vendor_name"], unique=False)

    op.create_table(
        "attendance",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("employee_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.Column("attendance_date", sa.Date(), nullable=False),
        sa.Column("status", _enum("attendance_status_enum"), nullable=False),
        sa.Column("working_hours", sa.Numeric(precision=4, scale=2), nullable=True),
        sa.Column("remarks", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["employee_id"], ["employees.id"], name="attendance_employee_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["project_id"], ["projects.id"], name="attendance_project_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="attendance_pkey"),
    )
    op.create_index("ix_attendance_attendance_date", "attendance", ["attendance_date"], unique=False)
    op.create_index("ix_attendance_employee_id", "attendance", ["employee_id"], unique=False)
    op.create_index("ix_attendance_id", "attendance", ["id"], unique=False)
    op.create_index("ix_attendance_project_id", "attendance", ["project_id"], unique=False)

    op.create_table(
        "employee_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("employee_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("log_date", sa.Date(), nullable=False),
        sa.Column("task_description", sa.String(length=1000), nullable=False),
        sa.Column("hours_worked", sa.Numeric(precision=4, scale=2), nullable=False),
        sa.Column("remarks", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["employee_id"], ["employees.id"], name="employee_logs_employee_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["project_id"], ["projects.id"], name="employee_logs_project_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="employee_logs_pkey"),
    )
    op.create_index("ix_employee_logs_employee_id", "employee_logs", ["employee_id"], unique=False)
    op.create_index("ix_employee_logs_id", "employee_logs", ["id"], unique=False)
    op.create_index("ix_employee_logs_log_date", "employee_logs", ["log_date"], unique=False)
    op.create_index("ix_employee_logs_project_id", "employee_logs", ["project_id"], unique=False)

    op.create_table(
        "expenses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("expense_category", _enum("expense_category_enum"), nullable=False),
        sa.Column("amount", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("expense_date", sa.Date(), nullable=False),
        sa.Column("remarks", sa.String(length=500), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], name="expenses_created_by_fkey"),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], name="expenses_project_id_fkey"),
        sa.PrimaryKeyConstraint("id", name="expenses_pkey"),
    )
    op.create_index("ix_expenses_expense_date", "expenses", ["expense_date"], unique=False)
    op.create_index("ix_expenses_id", "expenses", ["id"], unique=False)
    op.create_index("ix_expenses_project_id", "expenses", ["project_id"], unique=False)

    op.create_table(
        "material_stock",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("material_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("quantity_available", sa.Numeric(precision=12, scale=3), nullable=False),
        sa.Column("minimum_stock", sa.Numeric(precision=12, scale=3), nullable=False),
        sa.Column("last_updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["material_id"], ["materials.id"], name="material_stock_material_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["project_id"], ["projects.id"], name="material_stock_project_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="material_stock_pkey"),
    )
    op.create_index("ix_material_stock_id", "material_stock", ["id"], unique=False)
    op.create_index("ix_material_stock_material_id", "material_stock", ["material_id"], unique=False)
    op.create_index("ix_material_stock_project_id", "material_stock", ["project_id"], unique=False)

    op.create_table(
        "material_transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("material_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("transaction_type", _enum("transaction_type_enum"), nullable=False),
        sa.Column("quantity", sa.Numeric(precision=12, scale=3), nullable=False),
        sa.Column("transaction_date", sa.Date(), nullable=False),
        sa.Column("remarks", sa.String(length=500), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["created_by"], ["users.id"], name="material_transactions_created_by_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["material_id"], ["materials.id"], name="material_transactions_material_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["project_id"], ["projects.id"], name="material_transactions_project_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="material_transactions_pkey"),
    )
    op.create_index("ix_material_transactions_id", "material_transactions", ["id"], unique=False)
    op.create_index(
        "ix_material_transactions_material_id", "material_transactions", ["material_id"], unique=False
    )
    op.create_index(
        "ix_material_transactions_project_id", "material_transactions", ["project_id"], unique=False
    )
    op.create_index(
        "ix_material_transactions_transaction_date",
        "material_transactions",
        ["transaction_date"],
        unique=False,
    )


def downgrade() -> None:
    # Dropping a table also drops its indexes, constraints and OWNED BY sequences.
    for table in TABLES_DROP_ORDER:
        op.drop_table(table)

    bind = op.get_bind()
    for name in reversed(list(ENUMS)):
        postgresql.ENUM(name=name).drop(bind, checkfirst=False)
