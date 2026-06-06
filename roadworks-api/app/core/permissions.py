from enum import Enum
from typing import List
from fastapi import HTTPException, status


class Role(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    CONTRACTOR = "CONTRACTOR"
    PROJECT_MANAGER = "PROJECT_MANAGER"
    SITE_ENGINEER = "SITE_ENGINEER"
    SITE_SUPERVISOR = "SITE_SUPERVISOR"
    STORE_KEEPER = "STORE_KEEPER"
    ACCOUNTANT = "ACCOUNTANT"


# Role hierarchy: higher index = more restricted
ROLE_HIERARCHY = [
    Role.SUPER_ADMIN,
    Role.CONTRACTOR,
    Role.PROJECT_MANAGER,
    Role.SITE_ENGINEER,
    Role.SITE_SUPERVISOR,
    Role.STORE_KEEPER,
    Role.ACCOUNTANT,
]

# Role-based permissions mapping
ROLE_PERMISSIONS = {
    Role.SUPER_ADMIN: [
        "users:*", "employees:*", "projects:*", "materials:*",
        "stock:*", "vendors:*", "expenses:*", "attendance:*", "reports:*",
    ],
    Role.CONTRACTOR: [
        "employees:read", "employees:write",
        "projects:*", "materials:*", "stock:*",
        "vendors:*", "expenses:*", "attendance:*", "reports:*",
    ],
    Role.PROJECT_MANAGER: [
        "employees:read", "projects:read", "projects:write",
        "materials:read", "stock:read", "stock:write",
        "expenses:read", "expenses:write", "attendance:*", "reports:read",
    ],
    Role.SITE_ENGINEER: [
        "employees:read", "projects:read",
        "materials:read", "stock:read",
        "attendance:write", "attendance:read", "reports:read",
    ],
    Role.SITE_SUPERVISOR: [
        "employees:read", "attendance:write", "attendance:read",
        "projects:read", "reports:read",
    ],
    Role.STORE_KEEPER: [
        "materials:read", "stock:*", "vendors:read",
    ],
    Role.ACCOUNTANT: [
        "expenses:*", "reports:read", "vendors:read",
    ],
}


def require_roles(allowed_roles: List[Role]):
    """Dependency factory for role-based access control."""
    def check_role(current_user):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' is not permitted for this action.",
            )
        return current_user
    return check_role


def has_permission(user_role: str, permission: str) -> bool:
    """Check if a role has a specific permission."""
    role = Role(user_role)
    permissions = ROLE_PERMISSIONS.get(role, [])
    resource, action = permission.split(":")
    return (
        f"{resource}:*" in permissions
        or permission in permissions
        or f"*:{action}" in permissions
        or "*:*" in permissions
    )
