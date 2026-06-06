import { Box, Typography, Button } from "@mui/material";
import SearchOffIcon from "@mui/icons-material/SearchOff";
import type { ReactNode } from "react";

interface EmptyStateProps {
  title?: string;
  description?: string;
  icon?: ReactNode;
  actionLabel?: string;
  onAction?: () => void;
}

export function EmptyState({
  title = "No data found",
  description = "There are no records to display.",
  icon,
  actionLabel,
  onAction,
}: EmptyStateProps) {
  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      py={8}
      gap={2}
    >
      {icon || (
        <SearchOffIcon
          sx={{ fontSize: 64, color: "text.disabled", opacity: 0.5 }}
        />
      )}
      <Typography variant="h6" color="text.secondary">
        {title}
      </Typography>
      <Typography
        variant="body2"
        color="text.disabled"
        textAlign="center"
        maxWidth={320}
      >
        {description}
      </Typography>
      {actionLabel && onAction && (
        <Button variant="contained" onClick={onAction} sx={{ mt: 1 }}>
          {actionLabel}
        </Button>
      )}
    </Box>
  );
}
