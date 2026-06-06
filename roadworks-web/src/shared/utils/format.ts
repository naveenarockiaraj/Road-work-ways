/**
 * Format a number as Indian currency (INR).
 */
export function formatCurrency(
  value: number | string | null | undefined,
): string {
  if (value === null || value === undefined || value === "") return "₹0";
  const num = typeof value === "string" ? parseFloat(value) : value;
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(num);
}

/**
 * Format a date string or Date as DD/MM/YYYY.
 */
export function formatDate(value: string | Date | null | undefined): string {
  if (!value) return "-";
  const d = typeof value === "string" ? new Date(value) : value;
  if (isNaN(d.getTime())) return "-";
  return d.toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
}

/**
 * Format a number with comma separators.
 */
export function formatNumber(
  value: number | string | null | undefined,
): string {
  if (value === null || value === undefined) return "0";
  return new Intl.NumberFormat("en-IN").format(Number(value));
}

/**
 * Capitalize the first letter of a string.
 */
export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

/**
 * Convert SNAKE_CASE enum value to Title Case label.
 */
export function enumToLabel(value: string): string {
  return value
    .split("_")
    .map((word) => capitalize(word))
    .join(" ");
}
