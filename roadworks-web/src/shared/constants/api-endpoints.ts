const BASE = "/api/v1";

export const API_ENDPOINTS = {
  // Auth
  AUTH_LOGIN: `${BASE}/auth/login`,
  AUTH_LOGOUT: `${BASE}/auth/logout`,
  AUTH_ME: `${BASE}/auth/me`,

  // Employees
  EMPLOYEES: `${BASE}/employees`,
  EMPLOYEE: (id: number) => `${BASE}/employees/${id}`,

  // Attendance
  ATTENDANCE: `${BASE}/attendance`,

  // Projects
  PROJECTS: `${BASE}/projects`,
  PROJECT: (id: number) => `${BASE}/projects/${id}`,

  // Materials
  MATERIALS: `${BASE}/materials`,
  MATERIAL: (id: number) => `${BASE}/materials/${id}`,

  // Stock
  STOCK_BY_PROJECT: (projectId: number) => `${BASE}/stock/project/${projectId}`,
  STOCK_LOW: `${BASE}/stock/low-stock`,
  STOCK_TRANSACTION: `${BASE}/stock/transaction`,

  // Vendors
  VENDORS: `${BASE}/vendors`,
  VENDOR: (id: number) => `${BASE}/vendors/${id}`,

  // Expenses
  EXPENSES: `${BASE}/expenses`,
  EXPENSE: (id: number) => `${BASE}/expenses/${id}`,

  // Reports
  REPORT_DASHBOARD: `${BASE}/reports/dashboard`,
  REPORT_DAILY: `${BASE}/reports/daily`,
  REPORT_MONTHLY: `${BASE}/reports/monthly`,
  REPORT_MATERIAL_CONSUMPTION: `${BASE}/reports/material-consumption`,
} as const;
