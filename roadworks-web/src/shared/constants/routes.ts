export const ROUTES = {
  LOGIN: "/login",
  DASHBOARD: "/dashboard",

  EMPLOYEES: "/employees",
  EMPLOYEE_CREATE: "/employees/create",
  EMPLOYEE_DETAILS: "/employees/:id",

  ATTENDANCE: "/attendance",

  PROJECTS: "/projects",
  PROJECT_CREATE: "/projects/create",
  PROJECT_DETAILS: "/projects/:id",

  MATERIALS: "/materials",
  MATERIAL_STOCK: "/materials/stock",
  MATERIAL_INWARD: "/materials/inward",

  VENDORS: "/vendors",
  VENDOR_CREATE: "/vendors/create",

  EXPENSES: "/expenses",
  EXPENSE_ENTRY: "/expenses/entry",

  REPORT_DAILY: "/reports/daily",
  REPORT_MONTHLY: "/reports/monthly",
} as const;
