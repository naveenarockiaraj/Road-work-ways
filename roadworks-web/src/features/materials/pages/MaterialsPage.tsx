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
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import { useMaterialsQuery } from "../queries/use-materials-query";
import {
  useCreateMaterialMutation,
  useUpdateMaterialMutation,
  useDeleteMaterialMutation,
} from "../mutations/use-material-mutations";
import { DataTable, type Column } from "@shared/components/tables/DataTable";
import { ConfirmDialog } from "@shared/components/common/ConfirmDialog";
import { formatDate } from "@shared/utils/format";
import type { Material, MaterialCreate } from "../services/material.service";

const UNITS = [
  "Cubic Metre (m³)",
  "Square Metre (m²)",
  "Running Metre (RM)",
  "Metric Tonne (MT)",
  "Kilogram (kg)",
  "Litre (L)",
  "Number (Nos)",
  "Bag",
];
const INITIAL: MaterialCreate = {
  material_code: "",
  material_name: "",
  unit: "Metric Tonne (MT)",
  description: "",
};

export function MaterialsPage() {
  const [page, setPage] = useState(0);
  const [search, setSearch] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editTarget, setEditTarget] = useState<Material | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Material | null>(null);
  const [form, setForm] = useState<MaterialCreate>(INITIAL);

  const { data, isLoading } = useMaterialsQuery({
    page: page + 1,
    size: 10,
    search,
  });
  const createM = useCreateMaterialMutation();
  const updateM = useUpdateMaterialMutation(editTarget?.id ?? 0);
  const deleteM = useDeleteMaterialMutation();

  const columns: Column<Material>[] = [
    {
      id: "code",
      label: "Code",
      render: (r) => (
        <Typography variant="caption" fontFamily="monospace">
          {r.material_code}
        </Typography>
      ),
    },
    {
      id: "name",
      label: "Material Name",
      render: (r) => (
        <Typography variant="body2" fontWeight={600}>
          {r.material_name}
        </Typography>
      ),
    },
    { id: "unit", label: "Unit", render: (r) => r.unit },
    { id: "desc", label: "Description", render: (r) => r.description || "-" },
    {
      id: "updated",
      label: "Last Updated",
      render: (r) => formatDate(r.updated_at),
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
                setForm(r);
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
            Materials
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {data?.total ?? 0} materials
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            setEditTarget(null);
            setForm(INITIAL);
            setDialogOpen(true);
          }}
        >
          Add Material
        </Button>
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
        emptyTitle="No materials found"
      />

      <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          {editTarget ? "Edit Material" : "Add Material"}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 0.5 }}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                size="small"
                label="Material Code"
                value={form.material_code}
                onChange={(e) =>
                  setForm((f) => ({ ...f, material_code: e.target.value }))
                }
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                size="small"
                label="Material Name"
                value={form.material_name}
                onChange={(e) =>
                  setForm((f) => ({ ...f, material_name: e.target.value }))
                }
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                select
                fullWidth
                size="small"
                label="Unit"
                value={form.unit}
                onChange={(e) =>
                  setForm((f) => ({ ...f, unit: e.target.value }))
                }
              >
                {UNITS.map((u) => (
                  <MenuItem key={u} value={u}>
                    {u}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                size="small"
                label="Description"
                multiline
                rows={2}
                value={form.description}
                onChange={(e) =>
                  setForm((f) => ({ ...f, description: e.target.value }))
                }
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={() => {
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
                      setForm(INITIAL);
                    },
                  });
            }}
            disabled={createM.isPending || updateM.isPending}
          >
            {editTarget ? "Update" : "Create"}
          </Button>
        </DialogActions>
      </Dialog>

      <ConfirmDialog
        open={Boolean(deleteTarget)}
        message={`Delete material "${deleteTarget?.material_name}"?`}
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
