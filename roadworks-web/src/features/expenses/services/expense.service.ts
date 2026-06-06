import { httpClient } from "@shared/api/http-client";
import { API_ENDPOINTS } from "@shared/constants/api-endpoints";
import { buildUrl } from "@shared/api/endpoint-builder";
import type { PaginatedResponse } from "@shared/types/pagination.types";

export type ExpenseCategory =
  | "LABOUR"
  | "MATERIAL"
  | "EQUIPMENT"
  | "FUEL"
  | "TRANSPORT"
  | "MISCELLANEOUS"
  | "SUBCONTRACTOR"
  | "SITE_EXPENSES";

export interface Expense {
  id: number;
  project_id: number;
  expense_category: ExpenseCategory;
  amount: string;
  expense_date: string;
  remarks?: string;
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface ExpenseCreate {
  project_id: number;
  expense_category: ExpenseCategory;
  amount: number;
  expense_date: string;
  remarks?: string;
}

export type ExpenseUpdate = Partial<ExpenseCreate>;

export const expenseService = {
  async list(params: {
    page?: number;
    size?: number;
    project_id?: number;
    category?: string;
    from_date?: string;
    to_date?: string;
  }) {
    const url = buildUrl(API_ENDPOINTS.EXPENSES, params);
    const { data } = await httpClient.get<PaginatedResponse<Expense>>(url);
    return data;
  },
  async create(payload: ExpenseCreate) {
    const { data } = await httpClient.post<Expense>(
      API_ENDPOINTS.EXPENSES,
      payload,
    );
    return data;
  },
  async update(id: number, payload: ExpenseUpdate) {
    const { data } = await httpClient.put<Expense>(
      API_ENDPOINTS.EXPENSE(id),
      payload,
    );
    return data;
  },
  async remove(id: number) {
    await httpClient.delete(API_ENDPOINTS.EXPENSE(id));
  },
};
