import type { Edge, EdgeInput, Traversal, Vertex, VertexInput } from "../types/graph";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
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
      const body: { detail?: string } = await response.json();
      if (body.detail) message = body.detail;
    } catch {
      // Si la respuesta no es JSON, se conserva el mensaje HTTP.
    }
    throw new Error(message);
  }

  return response.json() as Promise<T>;
}

export const graphApi = {
  getVertices: () => request<Vertex[]>("/vertices"),
  getEdges: () => request<Edge[]>("/edges"),
  createVertex: (vertex: VertexInput) =>
    request<Vertex>("/vertices", {
      method: "POST",
      body: JSON.stringify(vertex),
    }),
  createEdge: (edge: EdgeInput) =>
    request<Edge>("/edges", {
      method: "POST",
      body: JSON.stringify(edge),
    }),
  breadthFirst: (start: number) =>
    request<Traversal>(`/traversals/breadth-first?start=${start}`),
  depthFirst: (start: number) =>
    request<Traversal>(`/traversals/depth-first?start=${start}`),
};
