import { Routes, Route, Navigate } from "react-router-dom";
import { ROUTES } from "@shared/constants/routes";
import { ProtectedRoute } from "@shared/components/common/ProtectedRoute";
import { AppLayout } from "@shared/components/layout/AppLayout";
import { LoginPage } from "@features/auth/pages/LoginPage";
import { DashboardPage } from "@features/dashboard/pages/DashboardPage";
import { EmployeesPage } from "@features/employees/pages/EmployeesPage";
import { AttendancePage } from "@features/attendance/pages/AttendancePage";
import { ProjectsPage } from "@features/projects/pages/ProjectsPage";
import { MaterialsPage } from "@features/materials/pages/MaterialsPage";
import { MaterialStockPage } from "@features/materials/pages/MaterialStockPage";
import { VendorsPage } from "@features/vendors/pages/VendorsPage";
import { ExpensesPage } from "@features/expenses/pages/ExpensesPage";
import { ReportsPage } from "@features/reports/pages/ReportsPage";

export function AppRouter() {
  return (
    <Routes>
      {/* Public */}
      <Route path={ROUTES.LOGIN} element={<LoginPage />} />

      {/* Protected */}
      <Route element={<ProtectedRoute />}>
        <Route element={<AppLayout />}>
          <Route path={ROUTES.DASHBOARD} element={<DashboardPage />} />
          <Route path={ROUTES.EMPLOYEES} element={<EmployeesPage />} />
          <Route path={ROUTES.EMPLOYEE_CREATE} element={<EmployeesPage />} />
          <Route path={ROUTES.EMPLOYEE_DETAILS} element={<EmployeesPage />} />
          <Route path={ROUTES.ATTENDANCE} element={<AttendancePage />} />
          <Route path={ROUTES.PROJECTS} element={<ProjectsPage />} />
          <Route path={ROUTES.PROJECT_CREATE} element={<ProjectsPage />} />
          <Route path={ROUTES.PROJECT_DETAILS} element={<ProjectsPage />} />
          <Route path={ROUTES.MATERIALS} element={<MaterialsPage />} />
          <Route path={ROUTES.MATERIAL_STOCK} element={<MaterialStockPage />} />
          <Route
            path={ROUTES.MATERIAL_INWARD}
            element={<MaterialStockPage />}
          />
          <Route path={ROUTES.VENDORS} element={<VendorsPage />} />
          <Route path={ROUTES.VENDOR_CREATE} element={<VendorsPage />} />
          <Route path={ROUTES.EXPENSES} element={<ExpensesPage />} />
          <Route path={ROUTES.EXPENSE_ENTRY} element={<ExpensesPage />} />
          <Route path={ROUTES.REPORT_DAILY} element={<ReportsPage />} />
          <Route path={ROUTES.REPORT_MONTHLY} element={<ReportsPage />} />
          <Route
            path="/"
            element={<Navigate to={ROUTES.DASHBOARD} replace />}
          />
        </Route>
      </Route>

      {/* Catch-all */}
      <Route path="*" element={<Navigate to={ROUTES.DASHBOARD} replace />} />
    </Routes>
  );
}
