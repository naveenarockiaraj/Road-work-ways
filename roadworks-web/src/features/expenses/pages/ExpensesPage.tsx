import { useState } from "react";
import {
  Box,
  Typography,
  Button,
  IconButton,
  Tooltip,
  Chip,
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
import DeleteIcon from "@mui/icons-material/Delete";
import { useExpensesQuery } from "../queries/use-expenses-query";
import {
  useCreateExpenseMutation,
  useDeleteExpenseMutation,
} from "../mutations/use-expense-mutations";
import { DataTable, type Column } from "@shared/components/tables/DataTable";
import { ConfirmDialog } from "@shared/components/common/ConfirmDialog";
import { formatCurrency, formatDate, enumToLabel } from "@shared/utils/format";
import type {
  Expense,
  ExpenseCreate,
  ExpenseCategory,
} from "../services/expense.service";

const CATEGORIES: ExpenseCategory[] = [
  "LABOUR",
  "MATERIAL",
  "EQUIPMENT",
  "FUEL",
  "TRANSPORT",
  "MISCELLANEOUS",
  "SUBCONTRACTOR",
  "SITE_EXPENSES",
];
const INITIAL: ExpenseCreate = {
  project_id: 0,
  expense_category: "MATERIAL",
  amount: 0,
  expense_date: new Date().toISOString().split("T")[0],
  remarks: "",
};

export function ExpensesPage() {
  const [page, setPage] = useState(0);
  const [catFilter, setCatFilter] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<Expense | null>(null);
  const [form, setForm] = useState<ExpenseCreate>(INITIAL);

  const { data, isLoading } = useExpensesQuery({
    page: page + 1,
    size: 10,
    category: catFilter || undefined,
  });
  const createM = useCreateExpenseMutation();
  const deleteM = useDeleteExpenseMutation();

  const total =
    data?.items.reduce((sum, e) => sum + parseFloat(e.amount), 0) ?? 0;

  const columns: Column<Expense>[] = [
    { id: "proj", label: "Project ID", render: (r) => r.project_id },
    {
      id: "cat",
      label: "Category",
      render: (r) => (
        <Chip
          label={enumToLabel(r.expense_category)}
          size="small"
          variant="outlined"
        />
      ),
    },
    {
      id: "amount",
      label: "Amount",
      align: "right",
      render: (r) => (
        <Typography fontWeight={600} color="error.main">
          {formatCurrency(r.amount)}
        </Typography>
      ),
    },
    { id: "date", label: "Date", render: (r) => formatDate(r.expense_date) },
    { id: "remarks", label: "Remarks", render: (r) => r.remarks || "-" },
    {
      id: "actions",
      label: "",
      align: "right",
      render: (r) => (
        <Tooltip title="Delete">
          <IconButton
            size="small"
            color="error"
            onClick={() => setDeleteTarget(r)}
          >
            <DeleteIcon fontSize="small" />
          </IconButton>
        </Tooltip>
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
            Expenses
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {data?.total ?? 0} records · Total: {formatCurrency(total)}
          </Typography>
        </Box>
        <Box display="flex" gap={1} alignItems="center">
          <Select
            size="small"
            value={catFilter}
            displayEmpty
            onChange={(e) => setCatFilter(e.target.value)}
            sx={{ minWidth: 160 }}
          >
            <MenuItem value="">All Categories</MenuItem>
            {CATEGORIES.map((c) => (
              <MenuItem key={c} value={c}>
                {enumToLabel(c)}
              </MenuItem>
            ))}
          </Select>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => {
              setForm(INITIAL);
              setDialogOpen(true);
            }}
          >
            Add Expense
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
        onPageChange={setPage}
        getRowKey={(r) => r.id}
        emptyTitle="No expenses found"
      />

      <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Add Expense</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 0.5 }}>
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
                select
                fullWidth
                size="small"
                label="Category"
                value={form.expense_category}
                onChange={(e) =>
                  setForm((f) => ({
                    ...f,
                    expense_category: e.target.value as ExpenseCategory,
                  }))
                }
              >
                {CATEGORIES.map((c) => (
                  <MenuItem key={c} value={c}>
                    {enumToLabel(c)}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                size="small"
                label="Amount (₹)"
                type="number"
                value={form.amount}
                onChange={(e) =>
                  setForm((f) => ({
                    ...f,
                    amount: parseFloat(e.target.value) || 0,
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
                value={form.expense_date}
                onChange={(e) =>
                  setForm((f) => ({ ...f, expense_date: e.target.value }))
                }
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                size="small"
                label="Remarks"
                multiline
                rows={2}
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

      <ConfirmDialog
        open={Boolean(deleteTarget)}
        message={`Delete this expense of ${formatCurrency(deleteTarget?.amount ?? 0)}?`}
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
