import { Card, CardContent, Typography, Box, Skeleton } from "@mui/material";
import type { ReactNode } from "react";

interface StatCardProps {
  label: string;
  value: string | number;
  icon: ReactNode;
  color: string;
  loading?: boolean;
  subtitle?: string;
}

export function StatCard({
  label,
  value,
  icon,
  color,
  loading,
  subtitle,
}: StatCardProps) {
  return (
    <Card
      sx={{
        borderRadius: 3,
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
        height: "100%",
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Box
          display="flex"
          alignItems="flex-start"
          justifyContent="space-between"
        >
          <Box>
            <Typography variant="body2" color="text.secondary" mb={0.5}>
              {label}
            </Typography>
            {loading ? (
              <Skeleton width={80} height={40} />
            ) : (
              <Typography variant="h4" fontWeight={700}>
                {value}
              </Typography>
            )}
            {subtitle && (
              <Typography
                variant="caption"
                color="text.secondary"
                mt={0.5}
                display="block"
              >
                {subtitle}
              </Typography>
            )}
          </Box>
          <Box
            sx={{
              bgcolor: `${color}20`,
              color,
              borderRadius: 2,
              p: 1.5,
              display: "flex",
              alignItems: "center",
              "& svg": { fontSize: 28 },
            }}
          >
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
}
