import { useState } from "react";
import { graphApi } from "../../services/graphApi";
import type { GraphKind, TraversalKind } from "../../types/graph";
import { Notice } from "../ui/Notice";

interface TraversalPanelProps {
  kind: GraphKind;
  vertexIds: string[];
  /** Traversal result in visit order, or null when it is cleared. */
  visitOrder: string[] | null;
  onResult: (visitOrder: string[] | null) => void;
}

/**
 * Run BFS / DFS on the graph shown and report the visit order.
 *
 * The result is lifted to the page through `onResult`, so the canvas can
 * draw the order as numbered badges on the nodes.
 *
 * @param props.kind Graph to traverse.
 * @param props.vertexIds Possible start vertices.
 * @param props.visitOrder Last result for this graph, or null.
 * @param props.onResult Receives the new result (or null to clear it).
 */
export function TraversalPanel({ kind, vertexIds, visitOrder, onResult }: TraversalPanelProps) {
  const [start, setStart] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const startId = vertexIds.includes(start) ? start : "";

  /**
   * Ask the backend for a traversal from the selected vertex.
   *
   * @param traversal "breadth-first" or "depth-first".
   */
  async function runTraversal(traversal: TraversalKind) {
    if (!startId) {
      setError("Selecciona un vértice inicial.");
      return;
    }
    setIsRunning(true);
    setError(null);
    try {
      const response = await graphApi.traverse(kind, traversal, startId);
      onResult(response.vertices);
    } catch (cause) {
      onResult(null);
      setError(cause instanceof Error ? cause.message : "No se pudo ejecutar el recorrido.");
    } finally {
      setIsRunning(false);
    }
  }

  return (
    <div className="space-y-3">
      <label htmlFor="traversal-start" className="block text-sm font-medium text-slate-300">
        Vértice inicial
      </label>
      <select
        id="traversal-start"
        value={startId}
        onChange={(event) => setStart(event.target.value)}
        className="field-control text-sm"
        disabled={!vertexIds.length}
      >
        <option value="">Selecciona un vértice</option>
        {vertexIds.map((vertexId) => (
          <option key={vertexId} value={vertexId}>
            {vertexId}
          </option>
        ))}
      </select>
      <div className="grid grid-cols-2 gap-2">
        <button
          type="button"
          onClick={() => void runTraversal("breadth-first")}
          disabled={isRunning || !vertexIds.length}
          className="button-secondary min-h-[42px] px-3 text-sm"
        >
          BFS · Anchura
        </button>
        <button
          type="button"
          onClick={() => void runTraversal("depth-first")}
          disabled={isRunning || !vertexIds.length}
          className="button-secondary min-h-[42px] px-3 text-sm"
        >
          DFS · Profundidad
        </button>
      </div>
      <p className="text-xs text-slate-500">
        Solo recorre aristas disponibles (un puente destruido corta el recorrido).
      </p>
      {error && <Notice tone="error">{error}</Notice>}
      {visitOrder && (
        <div className="rounded-lg border border-slate-800 p-3">
          <div className="mb-2 flex items-center justify-between">
            <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
              Orden visitado
            </p>
            <button
              type="button"
              onClick={() => onResult(null)}
              className="text-xs text-slate-400 hover:text-white"
            >
              Limpiar
            </button>
          </div>
          <p className="break-words text-sm text-indigo-200">{visitOrder.join(" → ")}</p>
        </div>
      )}
    </div>
  );
}
