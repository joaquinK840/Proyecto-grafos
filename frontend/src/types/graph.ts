/**
 * API contracts for the graph endpoints (`/api/graphs/{kind}/...`).
 * They mirror the backend response schemas one to one.
 */

/** Which graph of the scenario: elevated (GE) or maze (GM). */
export type GraphKind = "ge" | "gm";

/** Catalog of GE position types (backend `PositionType`). */
export type PositionType = "base" | "tower_candidate" | "transit" | "heliport";

/** Catalog of GM vertex roles (backend `MazeVertexRole`). */
export type MazeVertexRole = "normal" | "entry" | "exit";

/** Catalog of GE connection types (backend `ConnectionType`). */
export type ConnectionType = "path" | "bridge";

/** Vertex of the elevated graph GE. */
export interface VertexGE {
  id: string;
  x: number;
  y: number;
  position_type: PositionType;
  neighbors: string[];
}

/** Vertex of the maze graph GM. */
export interface VertexGM {
  id: string;
  x: number;
  y: number;
  role: MazeVertexRole;
  neighbors: string[];
}

/** Edge of GE (path or bridge). A `null` time means that transport is not allowed. */
export interface EdgeGE {
  id: string;
  v1: string;
  v2: string;
  connection_type: ConnectionType;
  foot_time: number | null;
  moto_time: number | null;
  max_resistance: number | null;
  current_resistance: number | null;
  enabled: boolean;
  available: boolean;
}

/** Corridor of GM. `travel_time` is t(e) = length / speed. */
export interface EdgeGM {
  id: string;
  v1: string;
  v2: string;
  length: number;
  speed: number;
  travel_time: number;
  enabled: boolean;
  available: boolean;
}

/** Vertices and edges of one graph. */
export interface GraphData<V, E> {
  vertices: V[];
  edges: E[];
}

export type ElevatedGraphData = GraphData<VertexGE, EdgeGE>;
export type MazeGraphData = GraphData<VertexGM, EdgeGM>;

/** Result of a BFS / DFS traversal: identifiers in visit order. */
export interface Traversal {
  vertices: string[];
}

/** Traversal algorithms offered by the API. */
export type TraversalKind = "breadth-first" | "depth-first";
