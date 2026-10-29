import { useState } from "react";
import { Box, useMediaQuery, useTheme } from "@mui/material";
import { Outlet } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { TopNavbar } from "./TopNavbar";

const DRAWER_WIDTH = 260;

export function AppLayout() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));
  const [desktopSidebarOpen, setDesktopSidebarOpen] = useState(true);
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);
  const sidebarOpen = isMobile ? mobileSidebarOpen : desktopSidebarOpen;

  const handleMenuClick = () => {
    if (isMobile) {
      setMobileSidebarOpen((open) => !open);
    } else {
      setDesktopSidebarOpen((open) => !open);
    }
  };

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
        onClose={() => setMobileSidebarOpen(false)}
        width={DRAWER_WIDTH}
        variant={isMobile ? "temporary" : "persistent"}
      />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          display: "flex",
          flexDirection: "column",
          minWidth: 0,
        }}
      >
        <TopNavbar onMenuClick={handleMenuClick} />
        <Box sx={{ flexGrow: 1, p: { xs: 2, sm: 3 }, pt: 2 }}>
          <Outlet />
        </Box>
      </Box>
    </Box>
  );
}
