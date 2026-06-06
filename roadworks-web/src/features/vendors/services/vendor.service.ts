import { httpClient } from "@shared/api/http-client";
import { API_ENDPOINTS } from "@shared/constants/api-endpoints";
import { buildUrl } from "@shared/api/endpoint-builder";
import type { PaginatedResponse } from "@shared/types/pagination.types";

export interface Vendor {
  id: number;
  vendor_name: string;
  contact_person: string;
  mobile_number: string;
  gst_number: string;
  address: string;
  created_at: string;
  updated_at: string;
}

export interface VendorCreate {
  vendor_name: string;
  contact_person: string;
  mobile_number: string;
  gst_number: string;
  address: string;
}

export type VendorUpdate = Partial<VendorCreate>;

export const vendorService = {
  async list(params: { page?: number; size?: number; search?: string }) {
    const url = buildUrl(API_ENDPOINTS.VENDORS, params);
    const { data } = await httpClient.get<PaginatedResponse<Vendor>>(url);
    return data;
  },
  async create(payload: VendorCreate) {
    const { data } = await httpClient.post<Vendor>(
      API_ENDPOINTS.VENDORS,
      payload,
    );
    return data;
  },
  async update(id: number, payload: VendorUpdate) {
    const { data } = await httpClient.put<Vendor>(
      API_ENDPOINTS.VENDOR(id),
      payload,
    );
    return data;
  },
  async remove(id: number) {
    await httpClient.delete(API_ENDPOINTS.VENDOR(id));
  },
};
