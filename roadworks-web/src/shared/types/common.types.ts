export interface SelectOption {
  label: string;
  value: string | number;
}

export type SortDirection = "asc" | "desc";

export interface TableColumn<T> {
  id: keyof T | string;
  label: string;
  sortable?: boolean;
  align?: "left" | "center" | "right";
  render?: (row: T) => React.ReactNode;
}
