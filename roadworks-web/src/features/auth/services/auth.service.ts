import { httpClient, tokenStorage } from "@shared/api/http-client";
import { API_ENDPOINTS } from "@shared/constants/api-endpoints";
import type { LoginResponse, AuthUser } from "../types/auth.types";

const USER_KEY = "rww_user";

export const authStorage = {
  getUser: (): AuthUser | null => {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? (JSON.parse(raw) as AuthUser) : null;
  },
  setUser: (user: AuthUser): void =>
    localStorage.setItem(USER_KEY, JSON.stringify(user)),
  removeUser: (): void => localStorage.removeItem(USER_KEY),
  clear: () => {
    tokenStorage.remove();
    localStorage.removeItem(USER_KEY);
  },
};

export const authService = {
  async login(username: string, password: string): Promise<LoginResponse> {
    const { data } = await httpClient.post<LoginResponse>(
      API_ENDPOINTS.AUTH_LOGIN,
      {
        username,
        password,
      },
    );
    tokenStorage.set(data.access_token);
    authStorage.setUser(data.user);
    return data;
  },

  async logout(): Promise<void> {
    try {
      await httpClient.post(API_ENDPOINTS.AUTH_LOGOUT);
    } catch {
      // ignore — clear storage regardless
    } finally {
      authStorage.clear();
    }
  },

  async getCurrentUser(): Promise<AuthUser> {
    const { data } = await httpClient.get<AuthUser>(API_ENDPOINTS.AUTH_ME);
    authStorage.setUser(data);
    return data;
  },
};
