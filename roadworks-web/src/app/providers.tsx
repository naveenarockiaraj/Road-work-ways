import { QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { Toaster } from "react-hot-toast";
import { queryClient } from "./query-client";
import { theme } from "./theme";
import type { ReactNode } from "react";

interface ProvidersProps {
  children: ReactNode;
}

export function Providers({ children }: ProvidersProps) {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: { background: "#1F2937", color: "#fff", borderRadius: 8 },
            success: { style: { background: "#2E7D32", color: "#fff" } },
            error: { style: { background: "#C62828", color: "#fff" } },
          }}
        />
        <ReactQueryDevtools initialIsOpen={false} />
      </ThemeProvider>
    </QueryClientProvider>
  );
}
