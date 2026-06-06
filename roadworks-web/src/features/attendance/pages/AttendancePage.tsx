import { useState } from "react";
import {
  Box,
  Typography,
  Button,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Grid,
  FormControl,
  Select,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { useAttendanceQuery } from "../queries/use-attendance-query";
import { useCreateAttendanceMutation } from "../mutations/use-attendance-mutations";
import { DataTable, type Column } from "@shared/components/tables/DataTable";
import { StatusChip } from "@shared/components/common/StatusChip";
import { formatDate } from "@shared/utils/format";
import type {
  Attendance,
  AttendanceCreate,
  AttendanceStatus,
} from "../services/attendance.service";

const STATUSES: AttendanceStatus[] = [
  "PRESENT",
  "ABSENT",
  "HALF_DAY",
  "LEAVE",
  "HOLIDAY",
];

const INITIAL: AttendanceCreate = {
  employee_id: 0,
  project_id: 0,
  attendance_date: new Date().toISOString().split("T")[0],
  status: "PRESENT",
  working_hours: 8,
  remarks: "",
};

export function AttendancePage() {
  const [dateFilter, setDateFilter] = useState(
    new Date().toISOString().split("T")[0],
  );
  const [dialogOpen, setDialogOpen] = useState(false);
  const [form, setForm] = useState<AttendanceCreate>(INITIAL);

  const { data = [], isLoading } = useAttendanceQuery({ date: dateFilter });
  const createM = useCreateAttendanceMutation();

  const columns: Column<Attendance>[] = [
    { id: "emp", label: "Employee ID", render: (r) => r.employee_id },
    { id: "proj", label: "Project ID", render: (r) => r.project_id },
    { id: "date", label: "Date", render: (r) => formatDate(r.attendance_date) },
    {
      id: "status",
      label: "Status",
      render: (r) => <StatusChip label={r.status} />,
    },
    {
      id: "hours",
      label: "Hours",
      align: "center",
      render: (r) => r.working_hours ?? "-",
    },
    { id: "remarks", label: "Remarks", render: (r) => r.remarks || "-" },
  ];

  return (
    <Box>
      <Box
        display="flex"
        alignItems="center"
        justifyContent="space-between"
        mb={3}
      >
        <Box>
          <Typography variant="h5" fontWeight={700}>
            Attendance
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {data.length} records
          </Typography>
        </Box>
        <Box display="flex" gap={1} alignItems="center">
          <TextField
            size="small"
            type="date"
            value={dateFilter}
            onChange={(e) => setDateFilter(e.target.value)}
            InputLabelProps={{ shrink: true }}
            label="Date"
          />
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setDialogOpen(true)}
          >
            Mark Attendance
          </Button>
        </Box>
      </Box>

      <DataTable
        columns={columns}
        rows={data}
        total={data.length}
        page={0}
        rowsPerPage={data.length || 10}
        loading={isLoading}
        onPageChange={() => {}}
        getRowKey={(r) => r.id}
        emptyTitle="No attendance records"
        emptyDescription="Mark attendance to see records here."
      />

      <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Mark Attendance</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 0.5 }}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                size="small"
                label="Employee ID"
                type="number"
                value={form.employee_id}
                onChange={(e) =>
                  setForm((f) => ({
                    ...f,
                    employee_id: parseInt(e.target.value) || 0,
                  }))
                }
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                size="small"
                label="Project ID"
                type="number"
                value={form.project_id}
                onChange={(e) =>
                  setForm((f) => ({
                    ...f,
                    project_id: parseInt(e.target.value) || 0,
                  }))
                }
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                size="small"
                label="Date"
                type="date"
                value={form.attendance_date}
                onChange={(e) =>
                  setForm((f) => ({ ...f, attendance_date: e.target.value }))
                }
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                select
                fullWidth
                size="small"
                label="Status"
                value={form.status}
                onChange={(e) =>
                  setForm((f) => ({
                    ...f,
                    status: e.target.value as AttendanceStatus,
                  }))
                }
              >
                {STATUSES.map((s) => (
                  <MenuItem key={s} value={s}>
                    {s}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                size="small"
                label="Working Hours"
                type="number"
                value={form.working_hours}
                onChange={(e) =>
                  setForm((f) => ({
                    ...f,
                    working_hours: parseFloat(e.target.value) || 0,
                  }))
                }
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                size="small"
                label="Remarks"
                value={form.remarks}
                onChange={(e) =>
                  setForm((f) => ({ ...f, remarks: e.target.value }))
                }
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={() =>
              createM.mutate(form, {
                onSuccess: () => {
                  setDialogOpen(false);
                  setForm(INITIAL);
                },
              })
            }
            disabled={createM.isPending}
          >
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
