/** Summary returned by `POST /api/scenarios/load` and `GET /api/scenarios/current`. */
export interface ScenarioSummary {
  name: string;
  ge_vertex_count: number;
  ge_edge_count: number;
  gm_vertex_count: number;
  gm_edge_count: number;
  base_id: string;
  entry_id: string;
  exit_id: string;
  shortest_maze_time: number;
  /** Vertex ids of the fastest GM route, from entry to exit. */
  shortest_maze_route: string[];
  /** Edge ids of the fastest GM route, in the same order. */
  shortest_maze_route_edges: string[];
}
