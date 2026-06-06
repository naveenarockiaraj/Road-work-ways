import { useMutation, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import {
  projectService,
  type ProjectCreate,
  type ProjectUpdate,
} from "../services/project.service";

export function useCreateProjectMutation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: ProjectCreate) => projectService.create(payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["projects"] });
      toast.success("Project created");
    },
    onError: (e: any) => toast.error(e.message || "Failed to create project"),
  });
}

export function useUpdateProjectMutation(id: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: ProjectUpdate) => projectService.update(id, payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["projects"] });
      toast.success("Project updated");
    },
    onError: (e: any) => toast.error(e.message || "Failed to update project"),
  });
}

export function useDeleteProjectMutation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => projectService.remove(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["projects"] });
      toast.success("Project deleted");
    },
    onError: (e: any) => toast.error(e.message || "Failed to delete project"),
  });
}
