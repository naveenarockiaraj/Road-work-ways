import { useQuery } from "@tanstack/react-query";
import { projectService } from "../services/project.service";

export function useProjectsQuery(params: {
  page: number;
  size: number;
  search?: string;
  status?: string;
}) {
  return useQuery({
    queryKey: ["projects", params],
    queryFn: () => projectService.list(params),
  });
}

export function useProjectQuery(id: number) {
  return useQuery({
    queryKey: ["projects", id],
    queryFn: () => projectService.get(id),
    enabled: id > 0,
  });
}
