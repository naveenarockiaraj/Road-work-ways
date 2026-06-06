import { useMutation, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import {
  employeeService,
  type EmployeeCreate,
  type EmployeeUpdate,
} from "../services/employee.service";

export function useCreateEmployeeMutation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: EmployeeCreate) => employeeService.create(payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["employees"] });
      toast.success("Employee created successfully");
    },
    onError: (e: any) => toast.error(e.message || "Failed to create employee"),
  });
}

export function useUpdateEmployeeMutation(id: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: EmployeeUpdate) =>
      employeeService.update(id, payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["employees"] });
      toast.success("Employee updated successfully");
    },
    onError: (e: any) => toast.error(e.message || "Failed to update employee"),
  });
}

export function useDeleteEmployeeMutation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => employeeService.remove(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["employees"] });
      toast.success("Employee deleted");
    },
    onError: (e: any) => toast.error(e.message || "Failed to delete employee"),
  });
}
