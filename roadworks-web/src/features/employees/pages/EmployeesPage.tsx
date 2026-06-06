import { useState } from "react";
import {
  Box,
  Typography,
  Button,
  Chip,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Grid,
  InputLabel,
  FormControl,
  Select,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import { useEmployeesQuery } from "../queries/use-employees-query";
import {
  useCreateEmployeeMutation,
  useUpdateEmployeeMutation,
  useDeleteEmployeeMutation,
} from "../mutations/use-employee-mutations";
import { DataTable, type Column } from "@shared/components/tables/DataTable";
import { StatusChip } from "@shared/components/common/StatusChip";
import { ConfirmDialog } from "@shared/components/common/ConfirmDialog";
import { formatCurrency, formatDate } from "@shared/utils/format";
import type { Employee, EmployeeCreate } from "../services/employee.service";
import { useForm } from "react-hook-form";

const INITIAL_FORM: EmployeeCreate = {
  employee_code: "",
  full_name: "",
  mobile_number: "",
  aadhaar_number: "",
  designation: "",
  daily_wage: 0,
  address: "",
  joining_date: new Date().toISOString().split("T")[0],
  status: "ACTIVE",
};

export function EmployeesPage() {
  const [page, setPage] = useState(0);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editTarget, setEditTarget] = useState<Employee | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Employee | null>(null);
  const [form, setForm] = useState<EmployeeCreate>(INITIAL_FORM);

  const { data, isLoading } = useEmployeesQuery({
    page: page + 1,
    size: 10,
    search,
    status: statusFilter || undefined,
  });
  const createMutation = useCreateEmployeeMutation();
  const updateMutation = useUpdateEmployeeMutation(editTarget?.id ?? 0);
  const deleteMutation = useDeleteEmployeeMutation();

  const columns: Column<Employee>[] = [
    {
      id: "code",
      label: "Code",
      render: (r) => (
        <Typography variant="caption" fontFamily="monospace">
          {r.employee_code}
        </Typography>
      ),
    },
    {
      id: "name",
      label: "Name",
      render: (r) => (
        <Typography variant="body2" fontWeight={600}>
          {r.full_name}
        </Typography>
      ),
    },
    { id: "designation", label: "Designation", render: (r) => r.designation },
    { id: "mobile", label: "Mobile", render: (r) => r.mobile_number },
    {
      id: "wage",
      label: "Daily Wage",
      align: "right",
      render: (r) => formatCurrency(r.daily_wage),
    },
    {
      id: "joining",
      label: "Joining Date",
      render: (r) => formatDate(r.joining_date),
    },
    {
      id: "status",
      label: "Status",
      render: (r) => <StatusChip label={r.status} />,
    },
    {
      id: "actions",
      label: "",
      align: "right",
      render: (r) => (
        <Box display="flex" justifyContent="flex-end" gap={0.5}>
          <Tooltip title="Edit">
            <IconButton
              size="small"
              onClick={() => {
                setEditTarget(r);
                setForm({ ...r, daily_wage: parseFloat(r.daily_wage) });
                setDialogOpen(true);
              }}
            >
              <EditIcon fontSize="small" />
            </IconButton>
          </Tooltip>
          <Tooltip title="Delete">
            <IconButton
              size="small"
              color="error"
              onClick={() => setDeleteTarget(r)}
            >
              <DeleteIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </Box>
      ),
    },
  ];

  const handleSave = () => {
    if (editTarget) {
      updateMutation.mutate(form, {
        onSuccess: () => {
          setDialogOpen(false);
          setEditTarget(null);
        },
      });
    } else {
      createMutation.mutate(form, {
        onSuccess: () => {
          setDialogOpen(false);
          setForm(INITIAL_FORM);
        },
      });
    }
  };

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
            Employees
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {data?.total ?? 0} total records
          </Typography>
        </Box>
        <Box display="flex" gap={1} alignItems="center">
          <FormControl size="small" sx={{ minWidth: 130 }}>
            <Select
              value={statusFilter}
              displayEmpty
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <MenuItem value="">All Status</MenuItem>
              <MenuItem value="ACTIVE">Active</MenuItem>
              <MenuItem value="INACTIVE">Inactive</MenuItem>
            </Select>
          </FormControl>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => {
              setEditTarget(null);
              setForm(INITIAL_FORM);
              setDialogOpen(true);
            }}
          >
            Add Employee
          </Button>
        </Box>
      </Box>

      <DataTable
        columns={columns}
        rows={data?.items ?? []}
        total={data?.total ?? 0}
        page={page}
        rowsPerPage={10}
        loading={isLoading}
        searchValue={search}
        onSearchChange={setSearch}
        onPageChange={setPage}
        getRowKey={(r) => r.id}
        emptyTitle="No employees found"
      />

      {/* Create/Edit Dialog */}
      <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          {editTarget ? "Edit Employee" : "Add Employee"}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 0.5 }}>
            {[
              { key: "employee_code", label: "Employee Code" },
              { key: "full_name", label: "Full Name" },
              { key: "mobile_number", label: "Mobile Number" },
              { key: "aadhaar_number", label: "Aadhaar Number" },
              { key: "designation", label: "Designation" },
              { key: "daily_wage", label: "Daily Wage (₹)", type: "number" },
              { key: "joining_date", label: "Joining Date", type: "date" },
            ].map(({ key, label, type }) => (
              <Grid item xs={12} sm={6} key={key}>
                <TextField
                  fullWidth
                  size="small"
                  label={label}
                  type={type || "text"}
                  value={(form as any)[key]}
                  onChange={(e) =>
                    setForm((f) => ({
                      ...f,
                      [key]:
                        type === "number"
                          ? parseFloat(e.target.value) || 0
                          : e.target.value,
                    }))
                  }
                  InputLabelProps={
                    type === "date" ? { shrink: true } : undefined
                  }
                />
              </Grid>
            ))}
            <Grid item xs={12} sm={6}>
              <TextField
                select
                fullWidth
                size="small"
                label="Status"
                value={form.status}
                onChange={(e) =>
                  setForm((f) => ({ ...f, status: e.target.value as any }))
                }
              >
                <MenuItem value="ACTIVE">Active</MenuItem>
                <MenuItem value="INACTIVE">Inactive</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                size="small"
                label="Address"
                multiline
                rows={2}
                value={form.address}
                onChange={(e) =>
                  setForm((f) => ({ ...f, address: e.target.value }))
                }
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleSave}
            disabled={createMutation.isPending || updateMutation.isPending}
          >
            {editTarget ? "Update" : "Create"}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Confirm Delete */}
      <ConfirmDialog
        open={Boolean(deleteTarget)}
        message={`Are you sure you want to delete ${deleteTarget?.full_name}?`}
        loading={deleteMutation.isPending}
        onConfirm={() => {
          if (deleteTarget)
            deleteMutation.mutate(deleteTarget.id, {
              onSuccess: () => setDeleteTarget(null),
            });
        }}
        onCancel={() => setDeleteTarget(null)}
      />
    </Box>
  );
}
