import { useQuery } from "@tanstack/react-query";
import { dashboardService } from "../services/dashboard.service";

export function useDashboardQuery() {
  return useQuery({
    queryKey: ["dashboard", "stats"],
    queryFn: dashboardService.getStats,
    staleTime: 60_000, // 1 minute
  });
}
