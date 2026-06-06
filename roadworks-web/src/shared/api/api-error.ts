export class ApiError extends Error {
  public readonly status: number;
  public readonly errorCode: string;
  public readonly details?: unknown[];

  constructor(
    status: number,
    message: string,
    errorCode = "API_ERROR",
    details?: unknown[],
  ) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.errorCode = errorCode;
    this.details = details;
  }

  get isUnauthorized() {
    return this.status === 401;
  }

  get isForbidden() {
    return this.status === 403;
  }

  get isNotFound() {
    return this.status === 404;
  }

  get isConflict() {
    return this.status === 409;
  }

  get isValidation() {
    return this.status === 422;
  }

  static fromAxiosError(error: any): ApiError {
    const response = error?.response;
    if (!response) {
      return new ApiError(0, "Network error. Please check your connection.");
    }
    const data = response.data;
    const message =
      data?.error || data?.detail || "An unexpected error occurred";
    const errorCode = data?.error_code || "API_ERROR";
    const details = data?.details;
    return new ApiError(response.status, message, errorCode, details);
  }
}
