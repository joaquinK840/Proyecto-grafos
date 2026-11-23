/** Point in screen (SVG) pixels. */
export interface ScreenPoint {
  x: number;
  y: number;
}

/**
 * Project scenario coordinates onto an SVG area.
 *
 * Both graphs share the same plane, so the vertices are drawn at their real
 * coordinates instead of using a force layout.
 *
 * @param points Points with scenario coordinates, keyed by id.
 * @param width Width of the drawing area in pixels.
 * @param height Height of the drawing area in pixels.
 * @param padding Free margin left on every side, in pixels.
 * @returns Screen position of every id.
 *
 * How it works: one scale factor is used for both axes (so distances and
 * angles are preserved), the drawing is centered in the area, and the Y axis
 * is flipped because in the scenario Y grows upwards but in SVG it grows
 * downwards. A degenerate range (all points on a line) is treated as 1.
 */
export function projectToScreen(
  points: { id: string; x: number; y: number }[],
  width: number,
  height: number,
  padding: number,
): Map<string, ScreenPoint> {
  const result = new Map<string, ScreenPoint>();
  if (points.length === 0) return result;

  const xs = points.map((point) => point.x);
  const ys = points.map((point) => point.y);
  const minX = Math.min(...xs);
  const minY = Math.min(...ys);
  const rangeX = Math.max(...xs) - minX || 1;
  const rangeY = Math.max(...ys) - minY || 1;

  const usableWidth = Math.max(width - 2 * padding, 1);
  const usableHeight = Math.max(height - 2 * padding, 1);
  const scale = Math.min(usableWidth / rangeX, usableHeight / rangeY);
  const offsetX = (width - rangeX * scale) / 2;
  const offsetY = (height - rangeY * scale) / 2;

  for (const point of points) {
    result.set(point.id, {
      x: offsetX + (point.x - minX) * scale,
      y: height - (offsetY + (point.y - minY) * scale),
    });
  }
  return result;
}
