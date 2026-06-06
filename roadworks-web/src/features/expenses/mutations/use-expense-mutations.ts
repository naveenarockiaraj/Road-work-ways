import { useMutation, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import {
  expenseService,
  type ExpenseCreate,
  type ExpenseUpdate,
} from "../services/expense.service";

export function useCreateExpenseMutation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (p: ExpenseCreate) => expenseService.create(p),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["expenses"] });
      qc.invalidateQueries({ queryKey: ["dashboard"] });
      toast.success("Expense recorded");
    },
    onError: (e: any) => toast.error(e.message),
  });
}

export function useDeleteExpenseMutation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => expenseService.remove(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["expenses"] });
      toast.success("Expense deleted");
    },
    onError: (e: any) => toast.error(e.message),
  });
}
