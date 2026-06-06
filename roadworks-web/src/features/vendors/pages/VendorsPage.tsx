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
  Grid,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import { useVendorsQuery } from "../queries/use-vendors-query";
import {
  useCreateVendorMutation,
  useUpdateVendorMutation,
  useDeleteVendorMutation,
} from "../mutations/use-vendor-mutations";
import { DataTable, type Column } from "@shared/components/tables/DataTable";
import { ConfirmDialog } from "@shared/components/common/ConfirmDialog";
import { formatDate } from "@shared/utils/format";
import type { Vendor, VendorCreate } from "../services/vendor.service";

const INITIAL: VendorCreate = {
  vendor_name: "",
  contact_person: "",
  mobile_number: "",
  gst_number: "",
  address: "",
};

export function VendorsPage() {
  const [page, setPage] = useState(0);
  const [search, setSearch] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editTarget, setEditTarget] = useState<Vendor | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Vendor | null>(null);
  const [form, setForm] = useState<VendorCreate>(INITIAL);

  const { data, isLoading } = useVendorsQuery({
    page: page + 1,
    size: 10,
    search,
  });
  const createM = useCreateVendorMutation();
  const updateM = useUpdateVendorMutation(editTarget?.id ?? 0);
  const deleteM = useDeleteVendorMutation();

  const setF = (k: keyof VendorCreate) => (e: any) =>
    setForm((f) => ({ ...f, [k]: e.target.value }));

  const columns: Column<Vendor>[] = [
    {
      id: "name",
      label: "Vendor Name",
      render: (r) => (
        <Typography variant="body2" fontWeight={600}>
          {r.vendor_name}
        </Typography>
      ),
    },
    { id: "contact", label: "Contact Person", render: (r) => r.contact_person },
    { id: "mobile", label: "Mobile", render: (r) => r.mobile_number },
    {
      id: "gst",
      label: "GST Number",
      render: (r) => (
        <Typography variant="caption" fontFamily="monospace">
          {r.gst_number}
        </Typography>
      ),
    },
    {
      id: "updated",
      label: "Updated",
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
            setForm(INITIAL);
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
            Vendors
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {data?.total ?? 0} vendors
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
          Add Vendor
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
        emptyTitle="No vendors found"
      />

      <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>{editTarget ? "Edit Vendor" : "Add Vendor"}</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 0.5 }}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                size="small"
                label="Vendor Name"
                value={form.vendor_name}
                onChange={setF("vendor_name")}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                size="small"
                label="Contact Person"
                value={form.contact_person}
                onChange={setF("contact_person")}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                size="small"
                label="Mobile Number"
                value={form.mobile_number}
                onChange={setF("mobile_number")}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                size="small"
                label="GST Number"
                value={form.gst_number}
                onChange={setF("gst_number")}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                size="small"
                label="Address"
                multiline
                rows={2}
                value={form.address}
                onChange={setF("address")}
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
        message={`Delete vendor "${deleteTarget?.vendor_name}"?`}
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
