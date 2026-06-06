import { httpClient } from "@shared/api/http-client";
import { API_ENDPOINTS } from "@shared/constants/api-endpoints";
import { buildUrl } from "@shared/api/endpoint-builder";
import type { PaginatedResponse } from "@shared/types/pagination.types";

export type ProjectStatus =
  | "PLANNING"
  | "IN_PROGRESS"
  | "ON_HOLD"
  | "COMPLETED"
  | "CANCELLED";
export type RoadType =
  | "NATIONAL_HIGHWAY"
  | "STATE_HIGHWAY"
  | "DISTRICT_ROAD"
  | "VILLAGE_ROAD"
  | "URBAN_ROAD";

export interface Project {
  id: number;
  project_code: string;
  project_name: string;
  road_type: RoadType;
  location: string;
  district: string;
  state: string;
  contract_value: string;
  start_date: string;
  end_date: string;
  status: ProjectStatus;
  created_at: string;
  updated_at: string;
}

export interface ProjectCreate {
  project_code: string;
  project_name: string;
  road_type: RoadType;
  location: string;
  district: string;
  state: string;
  contract_value: number;
  start_date: string;
  end_date: string;
  status?: ProjectStatus;
}

export type ProjectUpdate = Partial<ProjectCreate>;

export const projectService = {
  async list(params: {
    page?: number;
    size?: number;
    search?: string;
    status?: string;
  }) {
    const url = buildUrl(API_ENDPOINTS.PROJECTS, params);
    const { data } = await httpClient.get<PaginatedResponse<Project>>(url);
    return data;
  },
  async get(id: number) {
    const { data } = await httpClient.get<Project>(API_ENDPOINTS.PROJECT(id));
    return data;
  },
  async create(payload: ProjectCreate) {
    const { data } = await httpClient.post<Project>(
      API_ENDPOINTS.PROJECTS,
      payload,
    );
    return data;
  },
  async update(id: number, payload: ProjectUpdate) {
    const { data } = await httpClient.put<Project>(
      API_ENDPOINTS.PROJECT(id),
      payload,
    );
    return data;
  },
  async remove(id: number) {
    await httpClient.delete(API_ENDPOINTS.PROJECT(id));
  },
};
