import { useCallback, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { authService, authStorage } from "../services/auth.service";
import { tokenStorage } from "@shared/api/http-client";
import { ROUTES } from "@shared/constants/routes";
import type { AuthUser } from "../types/auth.types";

export function useAuth() {
  // Sync from localStorage — lightweight, no server fetch
  const token = tokenStorage.get();
  const storedUser = authStorage.getUser();
  const [user] = useState<AuthUser | null>(storedUser);

  const isLoading = false;
  const isAuthenticated = Boolean(token && user);

  const navigate = useNavigate();

  const logout = useCallback(async () => {
    await authService.logout();
    navigate(ROUTES.LOGIN, { replace: true });
  }, [navigate]);

  return { user, isAuthenticated, isLoading, logout };
}
