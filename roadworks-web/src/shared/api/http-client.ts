import axios from "axios";
import { ApiError } from "./api-error";

const TOKEN_KEY = "rww_access_token";

export const tokenStorage = {
  get: (): string | null => localStorage.getItem(TOKEN_KEY),
  set: (token: string): void => localStorage.setItem(TOKEN_KEY, token),
  remove: (): void => localStorage.removeItem(TOKEN_KEY),
};

export const httpClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "",
  timeout: 30_000,
  headers: { "Content-Type": "application/json" },
});

// Attach JWT on every request
httpClient.interceptors.request.use((config) => {
  const token = tokenStorage.get();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Transform error responses into ApiError instances
httpClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const apiError = ApiError.fromAxiosError(error);

    // Auto-logout on 401
    if (apiError.isUnauthorized) {
      tokenStorage.remove();
      const currentPath = window.location.pathname;
      if (currentPath !== "/login") {
        window.location.href = "/login";
      }
    }

    return Promise.reject(apiError);
  },
);
