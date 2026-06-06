import { httpClient } from "@shared/api/http-client";
import { API_ENDPOINTS } from "@shared/constants/api-endpoints";

export interface DashboardStats {
  total_projects: number;
  active_projects: number;
  total_employees: number;
  today_attendance: number;
  low_stock_count: number;
  today_expenses: number;
  monthly_expenses: number;
}

export const dashboardService = {
  async getStats(): Promise<DashboardStats> {
    const { data } = await httpClient.get<DashboardStats>(
      API_ENDPOINTS.REPORT_DASHBOARD,
    );
    return data;
  },
};
