import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { authService } from "../services/auth.service";
import { ROUTES } from "@shared/constants/routes";
import type { ApiError } from "@shared/api/api-error";

export function useLoginMutation() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      username,
      password,
    }: {
      username: string;
      password: string;
    }) => authService.login(username, password),
    onSuccess: (data) => {
      queryClient.setQueryData(["auth", "user"], data.user);
      toast.success(`Welcome, ${data.user.full_name}!`);
      navigate(ROUTES.DASHBOARD, { replace: true });
    },
    onError: (error: ApiError) => {
      toast.error(
        error.message || "Login failed. Please check your credentials.",
      );
    },
  });
}
