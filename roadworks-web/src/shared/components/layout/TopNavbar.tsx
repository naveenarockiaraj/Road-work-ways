import {
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  Box,
  Avatar,
  Menu,
  MenuItem,
  Divider,
  Tooltip,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import NotificationsIcon from "@mui/icons-material/Notifications";
import LogoutIcon from "@mui/icons-material/Logout";
import PersonIcon from "@mui/icons-material/Person";
import { useState } from "react";
import { useAuth } from "@features/auth/hooks/use-auth";
import { ROLE_LABELS } from "@shared/constants/roles";

interface TopNavbarProps {
  onMenuClick: () => void;
}

export function TopNavbar({ onMenuClick }: TopNavbarProps) {
  const { user, logout } = useAuth();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  return (
    <AppBar
      position="sticky"
      elevation={0}
      sx={{
        bgcolor: "background.paper",
        color: "text.primary",
        borderBottom: "1px solid",
        borderColor: "divider",
        zIndex: (theme) => theme.zIndex.drawer - 1,
      }}
    >
      <Toolbar>
        <IconButton edge="start" onClick={onMenuClick} sx={{ mr: 1 }}>
          <MenuIcon />
        </IconButton>

        <Box sx={{ flexGrow: 1 }} />

        {/* Notifications */}
        <Tooltip title="Notifications">
          <IconButton sx={{ mr: 1 }}>
            <NotificationsIcon />
          </IconButton>
        </Tooltip>

        {/* User Avatar */}
        <Box sx={{ display: "flex", alignItems: "center", gap: 1.5 }}>
          <Box
            sx={{ textAlign: "right", display: { xs: "none", sm: "block" } }}
          >
            <Typography variant="subtitle2" fontWeight={600} lineHeight={1.2}>
              {user?.full_name || "User"}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {user?.role ? ROLE_LABELS[user.role] : ""}
            </Typography>
          </Box>
          <Tooltip title="Account">
            <IconButton
              onClick={(e) => setAnchorEl(e.currentTarget)}
              sx={{ p: 0 }}
            >
              <Avatar
                sx={{
                  bgcolor: "primary.main",
                  width: 36,
                  height: 36,
                  fontSize: 14,
                }}
              >
                {user?.full_name?.charAt(0) || "U"}
              </Avatar>
            </IconButton>
          </Tooltip>
        </Box>

        {/* Account menu */}
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={() => setAnchorEl(null)}
          transformOrigin={{ horizontal: "right", vertical: "top" }}
          anchorOrigin={{ horizontal: "right", vertical: "bottom" }}
          PaperProps={{ sx: { minWidth: 180, mt: 1 } }}
        >
          <MenuItem disabled>
            <Typography variant="caption" color="text.secondary">
              {user?.email}
            </Typography>
          </MenuItem>
          <Divider />
          <MenuItem onClick={() => setAnchorEl(null)}>
            <PersonIcon fontSize="small" sx={{ mr: 1 }} />
            Profile
          </MenuItem>
          <MenuItem
            onClick={() => {
              setAnchorEl(null);
              logout();
            }}
            sx={{ color: "error.main" }}
          >
            <LogoutIcon fontSize="small" sx={{ mr: 1 }} />
            Logout
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
}
