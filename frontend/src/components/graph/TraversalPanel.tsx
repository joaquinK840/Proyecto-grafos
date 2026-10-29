import { useState } from "react";
import { graphApi } from "../../services/graphApi";
import type { Vertex } from "../../types/graph";
import { Notice } from "../ui/Notice";

interface TraversalPanelProps {
  vertices: Vertex[];
}

export function TraversalPanel({ vertices }: TraversalPanelProps) {
  const [start, setStart] = useState("");
  const [result, setResult] = useState<number[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState(false);

  async function runTraversal(kind: "breadth" | "depth") {
    if (!start) {
      setError("Selecciona un vértice inicial.");
      return;
    }
    setIsRunning(true);
    setError(null);
    setResult(null);
    try {
      const response =
        kind === "breadth"
          ? await graphApi.breadthFirst(Number(start))
          : await graphApi.depthFirst(Number(start));
      setResult(response.vertices);
    } catch (cause) {
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
        value={start}
        onChange={(event) => setStart(event.target.value)}
        className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-200"
        disabled={!vertices.length}
      >
        <option value="">Selecciona un vértice</option>
        {vertices.map((vertex) => (
          <option key={vertex.name} value={vertex.name}>Vértice {vertex.name}</option>
        ))}
      </select>
      <div className="grid grid-cols-2 gap-2">
        <button
          type="button"
          onClick={() => void runTraversal("breadth")}
          disabled={isRunning || !vertices.length}
          className="rounded-lg bg-slate-800 px-3 py-2 text-sm text-slate-200 hover:bg-slate-700 disabled:opacity-50"
        >
          BFS · Anchura
        </button>
        <button
          type="button"
          onClick={() => void runTraversal("depth")}
          disabled={isRunning || !vertices.length}
          className="rounded-lg bg-slate-800 px-3 py-2 text-sm text-slate-200 hover:bg-slate-700 disabled:opacity-50"
        >
          DFS · Profundidad
        </button>
      </div>
      {error && <Notice tone="error">{error}</Notice>}
      {result && (
        <div className="rounded-lg border border-slate-800 p-3">
          <p className="mb-2 text-xs font-medium uppercase tracking-wide text-slate-400">
            Orden visitado
          </p>
          <p className="break-words text-sm text-indigo-200">{result.join(" → ")}</p>
        </div>
      )}
    </div>
  );
}
