import { useMutation, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import {
  attendanceService,
  type AttendanceCreate,
} from "../services/attendance.service";

export function useCreateAttendanceMutation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: AttendanceCreate) =>
      attendanceService.create(payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["attendance"] });
      toast.success("Attendance marked");
    },
    onError: (e: any) => toast.error(e.message || "Failed to mark attendance"),
  });
}
