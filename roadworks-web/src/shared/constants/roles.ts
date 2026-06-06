export const ROLES = {
  SUPER_ADMIN: "SUPER_ADMIN",
  CONTRACTOR: "CONTRACTOR",
  PROJECT_MANAGER: "PROJECT_MANAGER",
  SITE_ENGINEER: "SITE_ENGINEER",
  SITE_SUPERVISOR: "SITE_SUPERVISOR",
  STORE_KEEPER: "STORE_KEEPER",
  ACCOUNTANT: "ACCOUNTANT",
} as const;

export type UserRole = (typeof ROLES)[keyof typeof ROLES];

export const ROLE_LABELS: Record<UserRole, string> = {
  SUPER_ADMIN: "Super Admin",
  CONTRACTOR: "Contractor",
  PROJECT_MANAGER: "Project Manager",
  SITE_ENGINEER: "Site Engineer",
  SITE_SUPERVISOR: "Site Supervisor",
  STORE_KEEPER: "Store Keeper",
  ACCOUNTANT: "Accountant",
};
