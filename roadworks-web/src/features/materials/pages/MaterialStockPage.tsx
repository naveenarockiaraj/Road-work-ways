import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import {
  Box,
  Typography,
  Button,
  Chip,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Grid,
} from "@mui/material";
import WarningIcon from "@mui/icons-material/Warning";
import AddIcon from "@mui/icons-material/Add";
import {
  stockService,
  type MaterialTransactionCreate,
  type TransactionType,
} from "../services/stock.service";
import { DataTable, type Column } from "@shared/components/tables/DataTable";
import { formatNumber, formatDate } from "@shared/utils/format";
import type { StockItem } from "../services/stock.service";

const TX_TYPES: TransactionType[] = [
  "INWARD",
  "OUTWARD",
  "RETURN",
  "ADJUSTMENT",
];

const INITIAL_TX: MaterialTransactionCreate = {
  material_id: 0,
  project_id: 0,
  transaction_type: "INWARD",
  quantity: 0,
  transaction_date: new Date().toISOString().split("T")[0],
  remarks: "",
};

export function MaterialStockPage() {
  const [projectId, setProjectId] = useState<number>(0);
  const [txOpen, setTxOpen] = useState(false);
  const [tx, setTx] = useState<MaterialTransactionCreate>(INITIAL_TX);
  const qc = useQueryClient();

  const { data: lowStock = [] } = useQuery({
    queryKey: ["stock", "low"],
    queryFn: stockService.getLowStock,
  });

  const { data: stockItems = [], isLoading } = useQuery({
    queryKey: ["stock", "project", projectId],
    queryFn: () => stockService.getByProject(projectId),
    enabled: projectId > 0,
  });

  const txMutation = useMutation({
    mutationFn: stockService.recordTransaction,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["stock"] });
      toast.success("Transaction recorded");
      setTxOpen(false);
      setTx(INITIAL_TX);
    },
    onError: (e: any) => toast.error(e.message),
  });

  const columns: Column<StockItem>[] = [
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
      label: "Material",
      render: (r) => (
        <Typography variant="body2" fontWeight={600}>
          {r.material_name}
        </Typography>
      ),
    },
    { id: "unit", label: "Unit", render: (r) => r.unit },
    {
      id: "qty",
      label: "Available",
      align: "right",
      render: (r) => formatNumber(r.quantity_available),
    },
    {
      id: "min",
      label: "Min Stock",
      align: "right",
      render: (r) => formatNumber(r.minimum_stock),
    },
    {
      id: "low",
      label: "Alert",
      render: (r) =>
        r.is_low_stock ? (
          <Chip label="Low" color="error" size="small" />
        ) : (
          <Chip label="OK" color="success" size="small" />
        ),
    },
    {
      id: "updated",
      label: "Last Updated",
      render: (r) => formatDate(r.last_updated),
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
            Material Stock
          </Typography>
          {lowStock.length > 0 && (
            <Typography
              variant="body2"
              color="error.main"
              display="flex"
              alignItems="center"
              gap={0.5}
            >
              <WarningIcon fontSize="small" /> {lowStock.length} low stock
              alert(s)
            </Typography>
          )}
        </Box>
        <Box display="flex" gap={1} alignItems="center">
          <TextField
            size="small"
            label="Project ID"
            type="number"
            value={projectId || ""}
            onChange={(e) => setProjectId(parseInt(e.target.value) || 0)}
            sx={{ width: 140 }}
          />
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setTxOpen(true)}
          >
            Record Transaction
          </Button>
        </Box>
      </Box>

      {projectId === 0 && (
        <Alert severity="info" sx={{ mb: 2 }}>
          Enter a project ID to view stock levels for that project.
        </Alert>
      )}

      {projectId > 0 && (
        <DataTable
          columns={columns}
          rows={stockItems}
          total={stockItems.length}
          page={0}
          rowsPerPage={stockItems.length || 10}
          loading={isLoading}
          onPageChange={() => {}}
          getRowKey={(r) => r.id}
          emptyTitle="No stock records"
          emptyDescription="No materials assigned to this project yet."
        />
      )}

      <Dialog
        open={txOpen}
        onClose={() => setTxOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Record Transaction</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 0.5 }}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                size="small"
                label="Material ID"
                type="number"
                value={tx.material_id}
                onChange={(e) =>
                  setTx((t) => ({
                    ...t,
                    material_id: parseInt(e.target.value) || 0,
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
                value={tx.project_id}
                onChange={(e) =>
                  setTx((t) => ({
                    ...t,
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
                label="Transaction Type"
                value={tx.transaction_type}
                onChange={(e) =>
                  setTx((t) => ({
                    ...t,
                    transaction_type: e.target.value as TransactionType,
                  }))
                }
              >
                {TX_TYPES.map((t) => (
                  <MenuItem key={t} value={t}>
                    {t}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                size="small"
                label="Quantity"
                type="number"
                value={tx.quantity}
                onChange={(e) =>
                  setTx((t) => ({
                    ...t,
                    quantity: parseFloat(e.target.value) || 0,
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
                value={tx.transaction_date}
                onChange={(e) =>
                  setTx((t) => ({ ...t, transaction_date: e.target.value }))
                }
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                size="small"
                label="Remarks"
                value={tx.remarks}
                onChange={(e) =>
                  setTx((t) => ({ ...t, remarks: e.target.value }))
                }
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setTxOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={() => txMutation.mutate(tx)}
            disabled={txMutation.isPending}
          >
            Record
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
