import { httpClient } from "@shared/api/http-client";
import { API_ENDPOINTS } from "@shared/constants/api-endpoints";
import { buildUrl } from "@shared/api/endpoint-builder";
import type { PaginatedResponse } from "@shared/types/pagination.types";

export interface Material {
  id: number;
  material_code: string;
  material_name: string;
  unit: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface MaterialCreate {
  material_code: string;
  material_name: string;
  unit: string;
  description?: string;
}

export type MaterialUpdate = Partial<MaterialCreate>;

export const materialService = {
  async list(params: { page?: number; size?: number; search?: string }) {
    const url = buildUrl(API_ENDPOINTS.MATERIALS, params);
    const { data } = await httpClient.get<PaginatedResponse<Material>>(url);
    return data;
  },
  async get(id: number) {
    const { data } = await httpClient.get<Material>(API_ENDPOINTS.MATERIAL(id));
    return data;
  },
  async create(payload: MaterialCreate) {
    const { data } = await httpClient.post<Material>(
      API_ENDPOINTS.MATERIALS,
      payload,
    );
    return data;
  },
  async update(id: number, payload: MaterialUpdate) {
    const { data } = await httpClient.put<Material>(
      API_ENDPOINTS.MATERIAL(id),
      payload,
    );
    return data;
  },
  async remove(id: number) {
    await httpClient.delete(API_ENDPOINTS.MATERIAL(id));
  },
};
