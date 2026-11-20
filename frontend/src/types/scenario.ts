export interface ScenarioLoadResponse {
  name: string;
  ge_vertex_count: number;
  ge_edge_count: number;
  gm_vertex_count: number;
  gm_edge_count: number;
  base_id: string;
  entry_id: string;
  exit_id: string;
  shortest_maze_time: number;
}
