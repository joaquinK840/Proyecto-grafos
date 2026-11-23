/** Minimal shape shared by GE and GM edges. */
interface UndirectedEdge {
  v1: string;
  v2: string;
}

/**
 * Return the edges that touch a vertex.
 *
 * @param edges Every edge of the graph.
 * @param vertexId Vertex to look for.
 * @returns Edges whose `v1` or `v2` is the vertex, in their original order.
 */
export function incidentEdges<E extends UndirectedEdge>(edges: E[], vertexId: string): E[] {
  return edges.filter((edge) => edge.v1 === vertexId || edge.v2 === vertexId);
}

/**
 * Return the endpoint at the other side of an undirected edge.
 *
 * @param edge Edge that touches `vertexId`.
 * @param vertexId One of its endpoints.
 * @returns The other endpoint identifier.
 */
export function oppositeEnd(edge: UndirectedEdge, vertexId: string): string {
  return edge.v1 === vertexId ? edge.v2 : edge.v1;
}
