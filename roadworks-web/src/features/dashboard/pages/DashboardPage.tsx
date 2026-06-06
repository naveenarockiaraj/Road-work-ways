import { Grid, Typography, Box, Button, Alert } from "@mui/material";
import EngineeringIcon from "@mui/icons-material/Engineering";
import PeopleIcon from "@mui/icons-material/People";
import EventAvailableIcon from "@mui/icons-material/EventAvailable";
import WarehouseIcon from "@mui/icons-material/Warehouse";
import AccountBalanceWalletIcon from "@mui/icons-material/AccountBalanceWallet";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import RefreshIcon from "@mui/icons-material/Refresh";
import { StatCard } from "../components/StatCard";
import { useDashboardQuery } from "../queries/use-dashboard-query";
import { formatCurrency } from "@shared/utils/format";
import { useAuth } from "@features/auth/hooks/use-auth";

export function DashboardPage() {
  const { user } = useAuth();
  const { data, isLoading, isError, refetch } = useDashboardQuery();

  return (
    <Box>
      {/* Page Header */}
      <Box
        display="flex"
        alignItems="center"
        justifyContent="space-between"
        mb={3}
      >
        <Box>
          <Typography variant="h5" fontWeight={700}>
            Dashboard
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Welcome back, {user?.full_name}
          </Typography>
        </Box>
        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={() => refetch()}
          size="small"
        >
          Refresh
        </Button>
      </Box>

      {isError && (
        <Alert severity="error" sx={{ mb: 3 }}>
          Failed to load dashboard data. Please refresh.
        </Alert>
      )}

      {/* KPI Cards */}
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={4} lg={3}>
          <StatCard
            label="Total Projects"
            value={data?.total_projects ?? 0}
            icon={<EngineeringIcon />}
            color="#1565C0"
            loading={isLoading}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4} lg={3}>
          <StatCard
            label="Active Projects"
            value={data?.active_projects ?? 0}
            icon={<TrendingUpIcon />}
            color="#2E7D32"
            loading={isLoading}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4} lg={3}>
          <StatCard
            label="Total Employees"
            value={data?.total_employees ?? 0}
            icon={<PeopleIcon />}
            color="#6A1B9A"
            loading={isLoading}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4} lg={3}>
          <StatCard
            label="Today Attendance"
            value={data?.today_attendance ?? 0}
            icon={<EventAvailableIcon />}
            color="#00838F"
            loading={isLoading}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4} lg={3}>
          <StatCard
            label="Low Stock Alerts"
            value={data?.low_stock_count ?? 0}
            icon={<WarehouseIcon />}
            color={data?.low_stock_count ? "#E53935" : "#43A047"}
            loading={isLoading}
            subtitle={data?.low_stock_count ? "Needs attention" : "All stocked"}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4} lg={3}>
          <StatCard
            label="Today Expenses"
            value={formatCurrency(data?.today_expenses ?? 0)}
            icon={<AccountBalanceWalletIcon />}
            color="#FF6F00"
            loading={isLoading}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4} lg={3}>
          <StatCard
            label="Monthly Expenses"
            value={formatCurrency(data?.monthly_expenses ?? 0)}
            icon={<AccountBalanceWalletIcon />}
            color="#BF360C"
            loading={isLoading}
            subtitle="Current month"
          />
        </Grid>
      </Grid>
    </Box>
  );
}
