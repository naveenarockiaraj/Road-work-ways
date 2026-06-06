import { useMutation, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import {
  materialService,
  type MaterialCreate,
  type MaterialUpdate,
} from "../services/material.service";

export function useCreateMaterialMutation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (p: MaterialCreate) => materialService.create(p),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["materials"] });
      toast.success("Material created");
    },
    onError: (e: any) => toast.error(e.message),
  });
}

export function useUpdateMaterialMutation(id: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (p: MaterialUpdate) => materialService.update(id, p),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["materials"] });
      toast.success("Material updated");
    },
    onError: (e: any) => toast.error(e.message),
  });
}

export function useDeleteMaterialMutation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => materialService.remove(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["materials"] });
      toast.success("Material deleted");
    },
    onError: (e: any) => toast.error(e.message),
  });
}
