import { httpClient } from "@shared/api/http-client";
import { API_ENDPOINTS } from "@shared/constants/api-endpoints";
import { buildUrl } from "@shared/api/endpoint-builder";
import type { PaginatedResponse } from "@shared/types/pagination.types";

export type EmployeeStatus = "ACTIVE" | "INACTIVE";

export interface Employee {
  id: number;
  employee_code: string;
  full_name: string;
  mobile_number: string;
  aadhaar_number: string;
  designation: string;
  daily_wage: string;
  address: string;
  joining_date: string;
  status: EmployeeStatus;
  created_at: string;
  updated_at: string;
}

export interface EmployeeCreate {
  employee_code: string;
  full_name: string;
  mobile_number: string;
  aadhaar_number: string;
  designation: string;
  daily_wage: number;
  address: string;
  joining_date: string;
  status?: EmployeeStatus;
}

export type EmployeeUpdate = Partial<EmployeeCreate>;

export const employeeService = {
  async list(params: {
    page?: number;
    size?: number;
    search?: string;
    status?: string;
  }) {
    const url = buildUrl(API_ENDPOINTS.EMPLOYEES, params);
    const { data } = await httpClient.get<PaginatedResponse<Employee>>(url);
    return data;
  },
  async get(id: number) {
    const { data } = await httpClient.get<Employee>(API_ENDPOINTS.EMPLOYEE(id));
    return data;
  },
  async create(payload: EmployeeCreate) {
    const { data } = await httpClient.post<Employee>(
      API_ENDPOINTS.EMPLOYEES,
      payload,
    );
    return data;
  },
  async update(id: number, payload: EmployeeUpdate) {
    const { data } = await httpClient.put<Employee>(
      API_ENDPOINTS.EMPLOYEE(id),
      payload,
    );
    return data;
  },
  async remove(id: number) {
    await httpClient.delete(API_ENDPOINTS.EMPLOYEE(id));
  },
};
