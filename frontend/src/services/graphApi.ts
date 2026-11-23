import type {
  EdgeGE,
  EdgeGM,
  ElevatedGraphData,
  GraphKind,
  MazeGraphData,
  Traversal,
  TraversalKind,
  VertexGE,
  VertexGM,
} from "../types/graph";
import { request } from "./httpClient";

/**
 * Fetch vertices and edges of one graph in parallel.
 *
 * @param kind "ge" or "gm".
 * @returns The graph data.
 */
async function fetchGraph<V, E>(kind: GraphKind) {
  const [vertices, edges] = await Promise.all([
    request<V[]>(`/graphs/${kind}/vertices`),
    request<E[]>(`/graphs/${kind}/edges`),
  ]);
  return { vertices, edges };
}

/** HTTP calls for the graphs of the loaded scenario. */
export const graphApi = {
  /** Vertices and edges of the elevated graph GE. */
  getElevatedGraph: (): Promise<ElevatedGraphData> => fetchGraph<VertexGE, EdgeGE>("ge"),

  /** Vertices and edges of the maze graph GM. */
  getMazeGraph: (): Promise<MazeGraphData> => fetchGraph<VertexGM, EdgeGM>("gm"),

  /**
   * Run a traversal on one graph.
   *
   * @param kind Graph to traverse.
   * @param traversal "breadth-first" or "depth-first".
   * @param start Identifier of the start vertex.
   */
  traverse: (kind: GraphKind, traversal: TraversalKind, start: string) =>
    request<Traversal>(
      `/graphs/${kind}/traversals/${traversal}?start=${encodeURIComponent(start)}`,
    ),
};
