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
  Select,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import { useProjectsQuery } from "../queries/use-projects-query";
import {
  useCreateProjectMutation,
  useUpdateProjectMutation,
  useDeleteProjectMutation,
} from "../mutations/use-project-mutations";
import { DataTable, type Column } from "@shared/components/tables/DataTable";
import { StatusChip } from "@shared/components/common/StatusChip";
import { ConfirmDialog } from "@shared/components/common/ConfirmDialog";
import { formatCurrency, formatDate, enumToLabel } from "@shared/utils/format";
import type {
  Project,
  ProjectCreate,
  RoadType,
  ProjectStatus,
} from "../services/project.service";

const ROAD_TYPES: RoadType[] = [
  "NATIONAL_HIGHWAY",
  "STATE_HIGHWAY",
  "DISTRICT_ROAD",
  "VILLAGE_ROAD",
  "URBAN_ROAD",
];
const PROJECT_STATUSES: ProjectStatus[] = [
  "PLANNING",
  "IN_PROGRESS",
  "ON_HOLD",
  "COMPLETED",
  "CANCELLED",
];

const INITIAL_FORM: ProjectCreate = {
  project_code: "",
  project_name: "",
  road_type: "DISTRICT_ROAD",
  location: "",
  district: "",
  state: "Telangana",
  contract_value: 0,
  start_date: new Date().toISOString().split("T")[0],
  end_date: new Date().toISOString().split("T")[0],
  status: "PLANNING",
};

export function ProjectsPage() {
  const [page, setPage] = useState(0);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editTarget, setEditTarget] = useState<Project | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Project | null>(null);
  const [form, setForm] = useState<ProjectCreate>(INITIAL_FORM);

  const { data, isLoading } = useProjectsQuery({
    page: page + 1,
    size: 10,
    search,
    status: statusFilter || undefined,
  });
  const createM = useCreateProjectMutation();
  const updateM = useUpdateProjectMutation(editTarget?.id ?? 0);
  const deleteM = useDeleteProjectMutation();

  const setField = (key: keyof ProjectCreate) => (e: any) =>
    setForm((f) => ({ ...f, [key]: e.target.value }));

  const columns: Column<Project>[] = [
    {
      id: "code",
      label: "Code",
      render: (r) => (
        <Typography variant="caption" fontFamily="monospace">
          {r.project_code}
        </Typography>
      ),
    },
    {
      id: "name",
      label: "Project Name",
      render: (r) => (
        <Typography variant="body2" fontWeight={600}>
          {r.project_name}
        </Typography>
      ),
    },
    { id: "road", label: "Road Type", render: (r) => enumToLabel(r.road_type) },
    {
      id: "location",
      label: "Location",
      render: (r) => `${r.district}, ${r.state}`,
    },
    {
      id: "value",
      label: "Contract Value",
      align: "right",
      render: (r) => formatCurrency(r.contract_value),
    },
    {
      id: "start",
      label: "Start Date",
      render: (r) => formatDate(r.start_date),
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
                setForm({ ...r, contract_value: parseFloat(r.contract_value) });
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
    const cb = {
      onSuccess: () => {
        setDialogOpen(false);
        setEditTarget(null);
      },
    };
    editTarget
      ? updateM.mutate(form, cb)
      : createM.mutate(form, {
          onSuccess: () => {
            setDialogOpen(false);
            setForm(INITIAL_FORM);
          },
        });
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
            Projects
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {data?.total ?? 0} total
          </Typography>
        </Box>
        <Box display="flex" gap={1}>
          <Select
            size="small"
            value={statusFilter}
            displayEmpty
            onChange={(e) => setStatusFilter(e.target.value)}
            sx={{ minWidth: 130 }}
          >
            <MenuItem value="">All Status</MenuItem>
            {PROJECT_STATUSES.map((s) => (
              <MenuItem key={s} value={s}>
                {enumToLabel(s)}
              </MenuItem>
            ))}
          </Select>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => {
              setEditTarget(null);
              setForm(INITIAL_FORM);
              setDialogOpen(true);
            }}
          >
            New Project
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
        emptyTitle="No projects found"
      />

      <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>{editTarget ? "Edit Project" : "New Project"}</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 0.5 }}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                size="small"
                label="Project Code"
                value={form.project_code}
                onChange={setField("project_code")}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                size="small"
                label="Project Name"
                value={form.project_name}
                onChange={setField("project_name")}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                select
                fullWidth
                size="small"
                label="Road Type"
                value={form.road_type}
                onChange={setField("road_type")}
              >
                {ROAD_TYPES.map((t) => (
                  <MenuItem key={t} value={t}>
                    {enumToLabel(t)}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                select
                fullWidth
                size="small"
                label="Status"
                value={form.status}
                onChange={setField("status")}
              >
                {PROJECT_STATUSES.map((s) => (
                  <MenuItem key={s} value={s}>
                    {enumToLabel(s)}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                size="small"
                label="Location"
                value={form.location}
                onChange={setField("location")}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                size="small"
                label="District"
                value={form.district}
                onChange={setField("district")}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                size="small"
                label="State"
                value={form.state}
                onChange={setField("state")}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                size="small"
                label="Contract Value (₹)"
                type="number"
                value={form.contract_value}
                onChange={(e) =>
                  setForm((f) => ({
                    ...f,
                    contract_value: parseFloat(e.target.value) || 0,
                  }))
                }
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                size="small"
                label="Start Date"
                type="date"
                value={form.start_date}
                onChange={setField("start_date")}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                size="small"
                label="End Date"
                type="date"
                value={form.end_date}
                onChange={setField("end_date")}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleSave}
            disabled={createM.isPending || updateM.isPending}
          >
            {editTarget ? "Update" : "Create"}
          </Button>
        </DialogActions>
      </Dialog>

      <ConfirmDialog
        open={Boolean(deleteTarget)}
        message={`Delete project "${deleteTarget?.project_name}"?`}
        loading={deleteM.isPending}
        onConfirm={() =>
          deleteTarget &&
          deleteM.mutate(deleteTarget.id, {
            onSuccess: () => setDeleteTarget(null),
          })
        }
        onCancel={() => setDeleteTarget(null)}
      />
    </Box>
  );
}
