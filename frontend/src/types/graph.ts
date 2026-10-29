export interface Vertex {
  name: number;
  available: boolean;
  neighbors: number[];
}

export interface Edge {
  source: number;
  target: number;
  weight: number;
}

export interface Traversal {
  vertices: number[];
}

export interface VertexInput {
  name: number;
}

export interface EdgeInput {
  source: number;
  target: number;
  weight: number;
}
