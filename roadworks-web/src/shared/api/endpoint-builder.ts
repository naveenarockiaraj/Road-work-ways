/**
 * Build URL with query parameters, omitting undefined/null values.
 */
export function buildUrl(
  base: string,
  params: Record<string, unknown> = {},
): string {
  const url = new URL(base, window.location.origin);
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      url.searchParams.set(key, String(value));
    }
  });
  // Return just the path + search (no origin)
  return url.pathname + url.search;
}
