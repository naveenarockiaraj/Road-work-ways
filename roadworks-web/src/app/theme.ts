import { createTheme } from "@mui/material/styles";

export const theme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: "#1565C0",
      light: "#1976D2",
      dark: "#0D47A1",
      contrastText: "#fff",
    },
    secondary: {
      main: "#FF6F00",
      light: "#FFA726",
      dark: "#E65100",
      contrastText: "#fff",
    },
    background: {
      default: "#F4F6F8",
      paper: "#FFFFFF",
    },
    success: { main: "#2E7D32" },
    warning: { main: "#F57C00" },
    error: { main: "#C62828" },
    grey: {
      50: "#F9FAFB",
      100: "#F3F4F6",
      200: "#E5E7EB",
      300: "#D1D5DB",
      400: "#9CA3AF",
      500: "#6B7280",
      600: "#4B5563",
      700: "#374151",
      800: "#1F2937",
      900: "#111827",
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: { fontWeight: 700 },
    h2: { fontWeight: 700 },
    h3: { fontWeight: 600 },
    h4: { fontWeight: 600 },
    h5: { fontWeight: 600 },
    h6: { fontWeight: 600 },
    subtitle1: { fontWeight: 500 },
    button: { textTransform: "none", fontWeight: 600 },
  },
  shape: { borderRadius: 8 },
  components: {
    MuiButton: {
      styleOverrides: {
        root: { borderRadius: 8, padding: "8px 20px" },
        contained: {
          boxShadow: "none",
          "&:hover": { boxShadow: "0 2px 8px rgba(0,0,0,0.15)" },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: { boxShadow: "0 1px 3px rgba(0,0,0,0.08)", borderRadius: 12 },
      },
    },
    MuiTextField: {
      defaultProps: { size: "small" },
    },
    MuiTableHead: {
      styleOverrides: {
        root: {
          "& .MuiTableCell-head": {
            backgroundColor: "#F3F4F6",
            fontWeight: 600,
            color: "#374151",
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: { root: { fontWeight: 500 } },
    },
  },
});
