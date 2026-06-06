import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  TextField,
  Tab,
  Tabs,
  Alert,
} from "@mui/material";
import { httpClient } from "@shared/api/http-client";
import { API_ENDPOINTS } from "@shared/constants/api-endpoints";
import { buildUrl } from "@shared/api/endpoint-builder";
import { formatCurrency, formatDate } from "@shared/utils/format";
import { DataTable, type Column } from "@shared/components/tables/DataTable";
import { LoadingSpinner } from "@shared/components/feedback/LoadingSpinner";

interface DailyReport {
  date: string;
  present_count: number;
  absent_count: number;
  half_day_count: number;
  total_wage: number;
}

interface MonthlyReport {
  month: string;
  year: number;
  total_employees_worked: number;
  total_labour_cost: number;
  total_expenses: number;
}

interface MaterialConsumption {
  material_name: string;
  material_code: string;
  unit: string;
  total_inward: number;
  total_outward: number;
  balance: number;
}

export function ReportsPage() {
  const [tab, setTab] = useState(0);
  const [dailyDate, setDailyDate] = useState(
    new Date().toISOString().split("T")[0],
  );
  const [monthlyDate, setMonthlyDate] = useState(
    new Date().toISOString().substring(0, 7),
  );
  const [projId, setProjId] = useState("");

  const { data: daily, isLoading: loadingDaily } = useQuery({
    queryKey: ["report", "daily", dailyDate],
    queryFn: async () => {
      const { data } = await httpClient.get(
        buildUrl(API_ENDPOINTS.REPORT_DAILY, { date: dailyDate }),
      );
      return data as DailyReport;
    },
    enabled: tab === 0,
  });

  const { data: monthly, isLoading: loadingMonthly } = useQuery({
    queryKey: ["report", "monthly", monthlyDate],
    queryFn: async () => {
      const [year, month] = monthlyDate.split("-");
      const { data } = await httpClient.get(
        buildUrl(API_ENDPOINTS.REPORT_MONTHLY, { year, month }),
      );
      return data as MonthlyReport;
    },
    enabled: tab === 1,
  });

  const { data: consumption = [], isLoading: loadingConsumption } = useQuery({
    queryKey: ["report", "material", projId],
    queryFn: async () => {
      const { data } = await httpClient.get(
        buildUrl(API_ENDPOINTS.REPORT_MATERIAL_CONSUMPTION, {
          project_id: projId,
        }),
      );
      return data as MaterialConsumption[];
    },
    enabled: tab === 2 && Boolean(projId),
  });

  const consumptionCols: Column<MaterialConsumption>[] = [
    {
      id: "code",
      label: "Code",
      render: (r) => (
        <Typography variant="caption" fontFamily="monospace">
          {r.material_code}
        </Typography>
      ),
    },
    { id: "name", label: "Material", render: (r) => r.material_name },
    { id: "unit", label: "Unit", render: (r) => r.unit },
    {
      id: "in",
      label: "Total Inward",
      align: "right",
      render: (r) => r.total_inward,
    },
    {
      id: "out",
      label: "Total Outward",
      align: "right",
      render: (r) => r.total_outward,
    },
    {
      id: "bal",
      label: "Balance",
      align: "right",
      render: (r) => (
        <Typography
          fontWeight={600}
          color={r.balance < 0 ? "error.main" : "success.main"}
        >
          {r.balance}
        </Typography>
      ),
    },
  ];

  return (
    <Box>
      <Typography variant="h5" fontWeight={700} mb={3}>
        Reports
      </Typography>

      <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 3 }}>
        <Tab label="Daily Report" />
        <Tab label="Monthly Report" />
        <Tab label="Material Consumption" />
      </Tabs>

      {/* Daily Report */}
      {tab === 0 && (
        <Box>
          <Box mb={2}>
            <TextField
              size="small"
              type="date"
              label="Date"
              value={dailyDate}
              onChange={(e) => setDailyDate(e.target.value)}
              InputLabelProps={{ shrink: true }}
            />
          </Box>
          {loadingDaily ? (
            <LoadingSpinner />
          ) : daily ? (
            <Grid container spacing={3}>
              {[
                {
                  label: "Present",
                  value: daily.present_count,
                  color: "#2E7D32",
                },
                {
                  label: "Absent",
                  value: daily.absent_count,
                  color: "#C62828",
                },
                {
                  label: "Half Day",
                  value: daily.half_day_count,
                  color: "#E65100",
                },
                {
                  label: "Total Wage",
                  value: formatCurrency(daily.total_wage),
                  color: "#1565C0",
                },
              ].map(({ label, value, color }) => (
                <Grid item xs={12} sm={6} md={3} key={label}>
                  <Card sx={{ borderRadius: 3 }}>
                    <CardContent>
                      <Typography variant="body2" color="text.secondary">
                        {label}
                      </Typography>
                      <Typography variant="h4" fontWeight={700} color={color}>
                        {value}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          ) : (
            <Alert severity="info">No data for {formatDate(dailyDate)}</Alert>
          )}
        </Box>
      )}

      {/* Monthly Report */}
      {tab === 1 && (
        <Box>
          <Box mb={2}>
            <TextField
              size="small"
              type="month"
              label="Month"
              value={monthlyDate}
              onChange={(e) => setMonthlyDate(e.target.value)}
              InputLabelProps={{ shrink: true }}
            />
          </Box>
          {loadingMonthly ? (
            <LoadingSpinner />
          ) : monthly ? (
            <Grid container spacing={3}>
              {[
                {
                  label: "Employees Worked",
                  value: monthly.total_employees_worked,
                },
                {
                  label: "Labour Cost",
                  value: formatCurrency(monthly.total_labour_cost),
                },
                {
                  label: "Total Expenses",
                  value: formatCurrency(monthly.total_expenses),
                },
              ].map(({ label, value }) => (
                <Grid item xs={12} sm={4} key={label}>
                  <Card sx={{ borderRadius: 3 }}>
                    <CardContent>
                      <Typography variant="body2" color="text.secondary">
                        {label}
                      </Typography>
                      <Typography variant="h4" fontWeight={700}>
                        {value}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          ) : (
            <Alert severity="info">No data for this month</Alert>
          )}
        </Box>
      )}

      {/* Material Consumption */}
      {tab === 2 && (
        <Box>
          <Box mb={2}>
            <TextField
              size="small"
              label="Project ID"
              type="number"
              value={projId}
              onChange={(e) => setProjId(e.target.value)}
            />
          </Box>
          {!projId && (
            <Alert severity="info" sx={{ mb: 2 }}>
              Enter a project ID to view material consumption.
            </Alert>
          )}
          <DataTable
            columns={consumptionCols}
            rows={consumption}
            total={consumption.length}
            page={0}
            rowsPerPage={consumption.length || 10}
            loading={loadingConsumption}
            onPageChange={() => {}}
            getRowKey={(r) => r.material_code}
            emptyTitle="No consumption data"
          />
        </Box>
      )}
    </Box>
  );
}
