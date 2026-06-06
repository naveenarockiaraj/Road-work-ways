import { useQuery } from "@tanstack/react-query";
import { vendorService } from "../services/vendor.service";

export function useVendorsQuery(params: {
  page: number;
  size: number;
  search?: string;
}) {
  return useQuery({
    queryKey: ["vendors", params],
    queryFn: () => vendorService.list(params),
  });
}
