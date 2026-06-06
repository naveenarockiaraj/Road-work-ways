import { useState } from "react";
import { Box } from "@mui/material";
import { Outlet } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { TopNavbar } from "./TopNavbar";

const DRAWER_WIDTH = 260;

export function AppLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <Box
      sx={{
        display: "flex",
        minHeight: "100vh",
        bgcolor: "background.default",
      }}
    >
      <Sidebar
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        width={DRAWER_WIDTH}
      />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          display: "flex",
          flexDirection: "column",
          ml: { sm: sidebarOpen ? `${DRAWER_WIDTH}px` : 0 },
          transition: "margin 0.2s ease",
          minWidth: 0,
        }}
      >
        <TopNavbar onMenuClick={() => setSidebarOpen((v) => !v)} />
        <Box sx={{ flexGrow: 1, p: 3, pt: 2 }}>
          <Outlet />
        </Box>
      </Box>
    </Box>
  );
}
