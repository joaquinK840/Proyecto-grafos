/**
 * View model shared by the generic graph components (canvas, legend,
 * details, edge list). The adapters in `src/presentation` translate the GE
 * and GM API data into these shapes, so the components never need to know
 * which graph they are drawing.
 */
import type { GraphKind } from "./graph";

/** Visual category of a node; each one has its own color. */
export type NodeTone =
  | "base"
  | "tower"
  | "transit"
  | "heliport"
  | "entry"
  | "exit"
  | "intersection";

/** Visual category of an edge. */
export type LinkTone = "path" | "bridge" | "corridor";

/** A vertex ready to be drawn at its real coordinates. */
export interface CanvasNode {
  id: string;
  x: number;
  y: number;
  tone: NodeTone;
  /** Text for the native tooltip. */
  tooltip: string;
}

/** An undirected edge ready to be drawn between two nodes. */
export interface CanvasLink {
  id: string;
  source: string;
  target: string;
  tone: LinkTone;
  /** Short text drawn at the midpoint (times, resistance...). */
  label: string;
  available: boolean;
  /** True when the edge belongs to the highlighted route. */
  highlighted: boolean;
}

/** One entry of the legend. */
export type LegendItem =
  | { kind: "node"; tone: NodeTone; label: string }
  | { kind: "link"; tone: LinkTone | "unavailable" | "route"; label: string };

/** A label/value pair shown in the vertex details. */
export interface DetailField {
  label: string;
  value: string;
}

/** One incident edge of the selected vertex. */
export interface ConnectionItem {
  edgeId: string;
  neighborId: string;
  summary: string;
  available: boolean;
  highlighted: boolean;
}

/** Everything the details panel shows for a vertex. */
export interface VertexDetail {
  id: string;
  typeLabel: string;
  tone: NodeTone;
  fields: DetailField[];
  connections: ConnectionItem[];
}

/** One row of the edge list. */
export interface EdgeRow {
  id: string;
  endpoints: string;
  typeLabel: string;
  metrics: string;
  statusLabel: string;
  available: boolean;
  highlighted: boolean;
}

/** Complete, graph-agnostic description of a graph view. */
export interface GraphView {
  kind: GraphKind;
  title: string;
  description: string;
  nodes: CanvasNode[];
  links: CanvasLink[];
  legend: LegendItem[];
  edgeRows: EdgeRow[];
  vertexIds: string[];
  /** Details of a vertex, or null if the id is not in the graph. */
  describeVertex: (vertexId: string) => VertexDetail | null;
}
