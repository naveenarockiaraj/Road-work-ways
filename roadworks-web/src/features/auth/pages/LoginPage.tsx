import { Navigate } from "react-router-dom";
import {
  Box,
  Card,
  CardContent,
  Typography,
  Divider,
  Stack,
} from "@mui/material";
import ConstructionIcon from "@mui/icons-material/Construction";
import { useAuth } from "../hooks/use-auth";
import { LoginForm } from "../components/LoginForm";
import { ROUTES } from "@shared/constants/routes";

export function LoginPage() {
  const { isAuthenticated } = useAuth();

  if (isAuthenticated) {
    return <Navigate to={ROUTES.DASHBOARD} replace />;
  }

  return (
    <Box
      sx={{
        minHeight: "100vh",
        background:
          "linear-gradient(135deg, #0D47A1 0%, #1565C0 50%, #1976D2 100%)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        p: 2,
      }}
    >
      <Card
        sx={{ width: "100%", maxWidth: 420, borderRadius: 3, boxShadow: 8 }}
      >
        <CardContent sx={{ p: { xs: 3, sm: 4 } }}>
          {/* Brand Header */}
          <Stack direction="row" alignItems="center" spacing={1.5} mb={3}>
            <Box
              sx={{
                bgcolor: "primary.main",
                borderRadius: 2,
                p: 1,
                display: "flex",
                alignItems: "center",
              }}
            >
              <ConstructionIcon sx={{ color: "#fff", fontSize: 28 }} />
            </Box>
            <Box>
              <Typography variant="h6" fontWeight={700} lineHeight={1.2}>
                Road Work Ways
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Construction Management System
              </Typography>
            </Box>
          </Stack>

          <Divider sx={{ mb: 3 }} />

          <Typography variant="h5" fontWeight={700} mb={0.5}>
            Welcome back
          </Typography>
          <Typography variant="body2" color="text.secondary" mb={3}>
            Sign in to access your dashboard
          </Typography>

          <LoginForm />
        </CardContent>
      </Card>
    </Box>
  );
}
