/** Error thrown by `request` that keeps the HTTP status code. */
export class ApiError extends Error {
  readonly status: number;

  /**
   * @param status HTTP status code of the failed response.
   * @param message Message taken from the backend `detail` field when present.
   */
  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

/**
 * Perform a JSON request against the backend (`/api` is proxied by Vite).
 *
 * @param path Path after `/api`, for example `/graphs/ge/vertices`.
 * @param init Optional fetch options (method, body...).
 * @returns The parsed JSON body.
 * @throws ApiError with the backend `detail` message when the status is not 2xx.
 */
export async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`/api${path}`, {
    ...init,
    headers: {
      ...(init?.body ? { "Content-Type": "application/json" } : {}),
      ...init?.headers,
    },
  });

  if (!response.ok) {
    let message = `Error ${response.status}: no se pudo completar la solicitud.`;
    try {
      const body: { detail?: unknown } = await response.json();
      if (typeof body.detail === "string") message = body.detail;
      else if (Array.isArray(body.detail)) message = describeValidationErrors(body.detail);
    } catch {
      // The body is not JSON: keep the generic HTTP message.
    }
    throw new ApiError(response.status, message);
  }

  return response.json() as Promise<T>;
}

/**
 * Turn the FastAPI/pydantic validation error list into a readable message.
 *
 * @param details Items with `loc` (path inside the JSON) and `msg`.
 * @returns One line per error, for example `ge → vertices → 0 → x: Input should be a valid number`.
 */
function describeValidationErrors(details: unknown[]): string {
  return details
    .map((item) => {
      const { loc, msg } = item as { loc?: unknown[]; msg?: string };
      const path = (loc ?? []).filter((part) => part !== "body").join(" → ");
      return path ? `${path}: ${msg ?? ""}` : (msg ?? "");
    })
    .join("\n");
}
