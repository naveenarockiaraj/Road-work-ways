import { Chip, type ChipProps } from "@mui/material";

interface StatusChipProps {
  label: string;
  color?: ChipProps["color"];
  size?: ChipProps["size"];
}

const STATUS_COLORS: Record<string, ChipProps["color"]> = {
  ACTIVE: "success",
  IN_PROGRESS: "info",
  PLANNING: "warning",
  ON_HOLD: "warning",
  COMPLETED: "success",
  CANCELLED: "error",
  INACTIVE: "default",
  PRESENT: "success",
  ABSENT: "error",
  HALF_DAY: "warning",
  LEAVE: "secondary",
  HOLIDAY: "default",
};

export function StatusChip({ label, color, size = "small" }: StatusChipProps) {
  const resolvedColor = color || STATUS_COLORS[label] || "default";
  return (
    <Chip
      label={label.replace(/_/g, " ")}
      color={resolvedColor}
      size={size}
      sx={{ fontWeight: 600, textTransform: "capitalize", fontSize: "0.7rem" }}
    />
  );
}
