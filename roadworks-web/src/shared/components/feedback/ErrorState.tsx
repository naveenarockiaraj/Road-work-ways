import { Box, Typography, Button, Alert } from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";

interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
}

export function ErrorState({
  title = "Something went wrong",
  message = "An error occurred while loading data. Please try again.",
  onRetry,
}: ErrorStateProps) {
  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      py={6}
      gap={2}
    >
      <Alert severity="error" sx={{ maxWidth: 480, width: "100%" }}>
        <Typography variant="subtitle1" fontWeight={600}>
          {title}
        </Typography>
        <Typography variant="body2">{message}</Typography>
      </Alert>
      {onRetry && (
        <Button
          variant="outlined"
          color="error"
          startIcon={<RefreshIcon />}
          onClick={onRetry}
        >
          Retry
        </Button>
      )}
    </Box>
  );
}
