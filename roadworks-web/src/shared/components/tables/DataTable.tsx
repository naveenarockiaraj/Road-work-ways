import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Paper,
  TextField,
  InputAdornment,
  Box,
  Typography,
  IconButton,
  Tooltip,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import { LoadingSpinner } from "../feedback/LoadingSpinner";
import { EmptyState } from "../feedback/EmptyState";
import type { ReactNode } from "react";

export interface Column<T> {
  id: string;
  label: string;
  align?: "left" | "center" | "right";
  render: (row: T) => ReactNode;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  rows: T[];
  total: number;
  page: number;
  rowsPerPage: number;
  loading?: boolean;
  searchValue?: string;
  onSearchChange?: (value: string) => void;
  onPageChange: (page: number) => void;
  onRowsPerPageChange?: (value: number) => void;
  getRowKey: (row: T) => string | number;
  actions?: ReactNode;
  emptyTitle?: string;
  emptyDescription?: string;
}

export function DataTable<T>({
  columns,
  rows,
  total,
  page,
  rowsPerPage,
  loading,
  searchValue,
  onSearchChange,
  onPageChange,
  onRowsPerPageChange,
  getRowKey,
  actions,
  emptyTitle,
  emptyDescription,
}: DataTableProps<T>) {
  return (
    <Box>
      {/* Toolbar */}
      {(onSearchChange !== undefined || actions) && (
        <Box
          display="flex"
          alignItems="center"
          justifyContent="space-between"
          mb={2}
          gap={2}
          flexWrap="wrap"
        >
          {onSearchChange && (
            <TextField
              size="small"
              placeholder="Search…"
              value={searchValue}
              onChange={(e) => onSearchChange(e.target.value)}
              sx={{ minWidth: 240 }}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon fontSize="small" />
                  </InputAdornment>
                ),
              }}
            />
          )}
          <Box display="flex" gap={1} ml="auto">
            {actions}
          </Box>
        </Box>
      )}

      <TableContainer
        component={Paper}
        variant="outlined"
        sx={{ borderRadius: 2 }}
      >
        <Table size="small">
          <TableHead>
            <TableRow>
              {columns.map((col) => (
                <TableCell
                  key={col.id}
                  align={col.align || "left"}
                  sx={{ fontWeight: 700 }}
                >
                  {col.label}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={columns.length}>
                  <LoadingSpinner />
                </TableCell>
              </TableRow>
            ) : rows.length === 0 ? (
              <TableRow>
                <TableCell colSpan={columns.length}>
                  <EmptyState
                    title={emptyTitle}
                    description={emptyDescription}
                  />
                </TableCell>
              </TableRow>
            ) : (
              rows.map((row) => (
                <TableRow key={getRowKey(row)} hover>
                  {columns.map((col) => (
                    <TableCell key={col.id} align={col.align || "left"}>
                      {col.render(row)}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
        <TablePagination
          component="div"
          count={total}
          page={page}
          rowsPerPage={rowsPerPage}
          onPageChange={(_, p) => onPageChange(p)}
          onRowsPerPageChange={
            onRowsPerPageChange
              ? (e) => onRowsPerPageChange(parseInt(e.target.value, 10))
              : undefined
          }
          rowsPerPageOptions={[10, 25, 50]}
        />
      </TableContainer>
    </Box>
  );
}
