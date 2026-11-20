import { useState, type ChangeEvent } from "react";
import { scenarioApi } from "../../services/scenarioApi";
import type { ScenarioLoadResponse } from "../../types/scenario";
import { Notice } from "../ui/Notice";

export function ScenarioLoader() {
  const [fileName, setFileName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [summary, setSummary] = useState<ScenarioLoadResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  async function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;

    setFileName(file.name);
    setError(null);
    setSummary(null);
    setIsLoading(true);

    try {
      const text = await file.text();
      let payload: unknown;
      try {
        payload = JSON.parse(text);
      } catch {
        throw new Error("El archivo no contiene JSON válido.");
      }
      setSummary(await scenarioApi.load(payload));
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "No se pudo cargar el escenario.");
    } finally {
      setIsLoading(false);
      event.target.value = "";
    }
  }

  return (
    <div className="space-y-3">
      <label htmlFor="scenario-file" className="block text-sm font-medium text-slate-300">
        Archivo JSON del escenario
      </label>
      <input
        id="scenario-file"
        type="file"
        accept=".json,application/json"
        onChange={(event) => void handleFileChange(event)}
        disabled={isLoading}
        className="block w-full rounded-lg border border-slate-700 bg-slate-950 text-sm text-slate-300 file:mr-3 file:border-0 file:bg-indigo-500 file:px-3 file:py-2 file:text-sm file:font-semibold file:text-white"
      />
      {fileName && (
        <p className="text-xs text-slate-500">Archivo seleccionado: {fileName}</p>
      )}
      {error && <Notice tone="error">{error}</Notice>}
      {summary && (
        <div className="rounded-lg border border-emerald-800 bg-emerald-950/30 p-3 text-sm text-emerald-200">
          <p className="font-semibold">{summary.name}</p>
          <p className="mt-1 text-xs text-emerald-300/80">
            GE: {summary.ge_vertex_count} vértices y {summary.ge_edge_count} aristas
          </p>
          <p className="text-xs text-emerald-300/80">
            GM: {summary.gm_vertex_count} vértices y {summary.gm_edge_count} aristas
          </p>
          <p className="text-xs text-emerald-300/80">
            Entrada {summary.entry_id} → salida {summary.exit_id}; tiempo mínimo {summary.shortest_maze_time}.
          </p>
        </div>
      )}
    </div>
  );
}
