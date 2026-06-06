import { httpClient } from "@shared/api/http-client";
import { API_ENDPOINTS } from "@shared/constants/api-endpoints";
import { buildUrl } from "@shared/api/endpoint-builder";

export type AttendanceStatus =
  | "PRESENT"
  | "ABSENT"
  | "HALF_DAY"
  | "LEAVE"
  | "HOLIDAY";

export interface Attendance {
  id: number;
  employee_id: number;
  project_id: number;
  attendance_date: string;
  status: AttendanceStatus;
  working_hours?: number;
  remarks?: string;
  created_at: string;
}

export interface AttendanceCreate {
  employee_id: number;
  project_id: number;
  attendance_date: string;
  status: AttendanceStatus;
  working_hours?: number;
  remarks?: string;
}

export const attendanceService = {
  async list(params: {
    employee_id?: number;
    project_id?: number;
    date?: string;
  }) {
    const url = buildUrl(API_ENDPOINTS.ATTENDANCE, params);
    const { data } = await httpClient.get<Attendance[]>(url);
    return data;
  },
  async create(payload: AttendanceCreate) {
    const { data } = await httpClient.post<Attendance>(
      API_ENDPOINTS.ATTENDANCE,
      payload,
    );
    return data;
  },
  async update(id: number, payload: Partial<AttendanceCreate>) {
    const { data } = await httpClient.put<Attendance>(
      `${API_ENDPOINTS.ATTENDANCE}/${id}`,
      payload,
    );
    return data;
  },
};
