import { useQuery } from "@tanstack/react-query";
import { materialService } from "../services/material.service";

export function useMaterialsQuery(params: {
  page: number;
  size: number;
  search?: string;
}) {
  return useQuery({
    queryKey: ["materials", params],
    queryFn: () => materialService.list(params),
  });
}
