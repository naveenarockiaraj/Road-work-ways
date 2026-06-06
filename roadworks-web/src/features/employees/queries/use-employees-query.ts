import { useQuery } from "@tanstack/react-query";
import { employeeService } from "../services/employee.service";

interface Params {
  page: number;
  size: number;
  search?: string;
  status?: string;
}

export function useEmployeesQuery(params: Params) {
  return useQuery({
    queryKey: ["employees", params],
    queryFn: () => employeeService.list(params),
  });
}

export function useEmployeeQuery(id: number) {
  return useQuery({
    queryKey: ["employees", id],
    queryFn: () => employeeService.get(id),
    enabled: id > 0,
  });
}
