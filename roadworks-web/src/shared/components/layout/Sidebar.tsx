import { useNavigate, useLocation } from "react-router-dom";
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  Divider,
  Box,
  Collapse,
} from "@mui/material";
import DashboardIcon from "@mui/icons-material/Dashboard";
import PeopleIcon from "@mui/icons-material/People";
import EventIcon from "@mui/icons-material/Event";
import EngineeringIcon from "@mui/icons-material/Engineering";
import InventoryIcon from "@mui/icons-material/Inventory";
import StoreIcon from "@mui/icons-material/Store";
import ReceiptIcon from "@mui/icons-material/Receipt";
import AssessmentIcon from "@mui/icons-material/Assessment";
import BusinessIcon from "@mui/icons-material/Business";
import { ROUTES } from "@shared/constants/routes";

interface SidebarProps {
  open: boolean;
  onClose: () => void;
  width: number;
}

const navItems = [
  { label: "Dashboard", icon: <DashboardIcon />, path: ROUTES.DASHBOARD },
  { label: "Projects", icon: <EngineeringIcon />, path: ROUTES.PROJECTS },
  { label: "Employees", icon: <PeopleIcon />, path: ROUTES.EMPLOYEES },
  { label: "Attendance", icon: <EventIcon />, path: ROUTES.ATTENDANCE },
  { label: "Materials", icon: <InventoryIcon />, path: ROUTES.MATERIALS },
  { label: "Stock", icon: <StoreIcon />, path: ROUTES.MATERIAL_STOCK },
  { label: "Vendors", icon: <BusinessIcon />, path: ROUTES.VENDORS },
  { label: "Expenses", icon: <ReceiptIcon />, path: ROUTES.EXPENSES },
  { label: "Reports", icon: <AssessmentIcon />, path: ROUTES.REPORT_DAILY },
];

export function Sidebar({ open, onClose, width }: SidebarProps) {
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path: string) =>
    path === ROUTES.DASHBOARD
      ? location.pathname === path
      : location.pathname.startsWith(path);

  return (
    <Drawer
      variant="persistent"
      anchor="left"
      open={open}
      sx={{
        width,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width,
          boxSizing: "border-box",
          background: "linear-gradient(180deg, #0D47A1 0%, #1565C0 100%)",
          color: "#fff",
          border: "none",
        },
      }}
    >
      {/* Brand */}
      <Toolbar sx={{ px: 2, py: 1.5 }}>
        <Box>
          <Typography
            variant="h6"
            fontWeight={700}
            color="#fff"
            lineHeight={1.2}
          >
            Road Work Ways
          </Typography>
          <Typography variant="caption" sx={{ color: "rgba(255,255,255,0.7)" }}>
            Construction Management
          </Typography>
        </Box>
      </Toolbar>

      <Divider sx={{ borderColor: "rgba(255,255,255,0.15)" }} />

      <List sx={{ pt: 1 }}>
        {navItems.map((item) => {
          const active = isActive(item.path);
          return (
            <ListItem key={item.path} disablePadding sx={{ px: 1, mb: 0.25 }}>
              <ListItemButton
                onClick={() => navigate(item.path)}
                selected={active}
                sx={{
                  borderRadius: 2,
                  color: active ? "#fff" : "rgba(255,255,255,0.75)",
                  bgcolor: active ? "rgba(255,255,255,0.18)" : "transparent",
                  "&:hover": {
                    bgcolor: "rgba(255,255,255,0.12)",
                    color: "#fff",
                  },
                  "&.Mui-selected": {
                    bgcolor: "rgba(255,255,255,0.18)",
                    "&:hover": { bgcolor: "rgba(255,255,255,0.22)" },
                  },
                }}
              >
                <ListItemIcon sx={{ color: "inherit", minWidth: 40 }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText
                  primary={item.label}
                  primaryTypographyProps={{
                    fontSize: 14,
                    fontWeight: active ? 600 : 400,
                  }}
                />
              </ListItemButton>
            </ListItem>
          );
        })}
      </List>
    </Drawer>
  );
}
