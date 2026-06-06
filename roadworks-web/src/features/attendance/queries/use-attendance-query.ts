import { useQuery } from "@tanstack/react-query";
import { attendanceService } from "../services/attendance.service";

export function useAttendanceQuery(params: {
  employee_id?: number;
  project_id?: number;
  date?: string;
}) {
  return useQuery({
    queryKey: ["attendance", params],
    queryFn: () => attendanceService.list(params),
  });
}
