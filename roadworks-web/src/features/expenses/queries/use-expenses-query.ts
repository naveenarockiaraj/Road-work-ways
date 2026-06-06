import { useQuery } from "@tanstack/react-query";
import { expenseService } from "../services/expense.service";

interface Params {
  page: number;
  size: number;
  project_id?: number;
  category?: string;
  from_date?: string;
  to_date?: string;
}

export function useExpensesQuery(params: Params) {
  return useQuery({
    queryKey: ["expenses", params],
    queryFn: () => expenseService.list(params),
  });
}
