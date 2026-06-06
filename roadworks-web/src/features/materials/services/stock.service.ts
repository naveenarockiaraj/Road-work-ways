import { httpClient } from "@shared/api/http-client";
import { API_ENDPOINTS } from "@shared/constants/api-endpoints";
import { buildUrl } from "@shared/api/endpoint-builder";
import type { PaginatedResponse } from "@shared/types/pagination.types";

export interface StockItem {
  id: number;
  material_id: number;
  project_id: number;
  quantity_available: string;
  minimum_stock: string;
  last_updated: string;
  material_name: string;
  material_code: string;
  unit: string;
  is_low_stock: boolean;
}

export type TransactionType = "INWARD" | "OUTWARD" | "RETURN" | "ADJUSTMENT";

export interface MaterialTransactionCreate {
  material_id: number;
  project_id: number;
  transaction_type: TransactionType;
  quantity: number;
  transaction_date: string;
  remarks?: string;
}

export const stockService = {
  async getByProject(projectId: number) {
    const { data } = await httpClient.get<StockItem[]>(
      API_ENDPOINTS.STOCK_BY_PROJECT(projectId),
    );
    return data;
  },
  async getLowStock() {
    const { data } = await httpClient.get<StockItem[]>(API_ENDPOINTS.STOCK_LOW);
    return data;
  },
  async recordTransaction(payload: MaterialTransactionCreate) {
    const { data } = await httpClient.post(
      API_ENDPOINTS.STOCK_TRANSACTION,
      payload,
    );
    return data;
  },
};
