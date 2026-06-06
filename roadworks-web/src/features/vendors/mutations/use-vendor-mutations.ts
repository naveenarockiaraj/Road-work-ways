import { useMutation, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import {
  vendorService,
  type VendorCreate,
  type VendorUpdate,
} from "../services/vendor.service";

export function useCreateVendorMutation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (p: VendorCreate) => vendorService.create(p),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["vendors"] });
      toast.success("Vendor created");
    },
    onError: (e: any) => toast.error(e.message),
  });
}

export function useUpdateVendorMutation(id: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (p: VendorUpdate) => vendorService.update(id, p),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["vendors"] });
      toast.success("Vendor updated");
    },
    onError: (e: any) => toast.error(e.message),
  });
}

export function useDeleteVendorMutation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => vendorService.remove(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["vendors"] });
      toast.success("Vendor deleted");
    },
    onError: (e: any) => toast.error(e.message),
  });
}
