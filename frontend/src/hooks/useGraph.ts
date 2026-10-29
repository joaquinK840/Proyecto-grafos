import { useCallback, useEffect, useState } from "react";
import { graphApi } from "../services/graphApi";
import type { Edge, EdgeInput, Vertex, VertexInput } from "../types/graph";

export function useGraph() {
  const [vertices, setVertices] = useState<Vertex[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [nextVertices, nextEdges] = await Promise.all([
        graphApi.getVertices(),
        graphApi.getEdges(),
      ]);
      setVertices(nextVertices);
      setEdges(nextEdges);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Error al cargar el grafo.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const createVertex = useCallback(
    async (input: VertexInput) => {
      await graphApi.createVertex(input);
      await refresh();
    },
    [refresh],
  );

  const createEdge = useCallback(
    async (input: EdgeInput) => {
      await graphApi.createEdge(input);
      await refresh();
    },
    [refresh],
  );

  return { vertices, edges, isLoading, error, refresh, createVertex, createEdge };
}
