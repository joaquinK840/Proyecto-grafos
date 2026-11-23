const numberFormat = new Intl.NumberFormat("es-CO", { maximumFractionDigits: 2 });

/**
 * Format a number with at most two decimals using the Spanish locale.
 *
 * @param value Number to format.
 * @returns For example `2,5`.
 */
export function formatNumber(value: number): string {
  return numberFormat.format(value);
}

/**
 * Format a duration in seconds, or a dash when it does not apply.
 *
 * @param seconds Duration, or `null` when the transport is not allowed.
 * @returns For example `2,5 s` or `—`.
 */
export function formatSeconds(seconds: number | null): string {
  return seconds === null ? "—" : `${formatNumber(seconds)} s`;
}

/**
 * Format a pair of coordinates.
 *
 * @param x Horizontal coordinate.
 * @param y Vertical coordinate.
 * @returns For example `(1, 2,5)`.
 */
export function formatCoordinates(x: number, y: number): string {
  return `(${formatNumber(x)}, ${formatNumber(y)})`;
}
