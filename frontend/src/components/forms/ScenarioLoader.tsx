import { useState, type ChangeEvent } from "react";
import type { ScenarioSummary } from "../../types/scenario";
import { formatSeconds } from "../../presentation/formatters";
import { Notice } from "../ui/Notice";

interface ScenarioLoaderProps {
  /** Summary of the scenario currently loaded, if any. */
  summary: ScenarioSummary | null;
  /** Sends the parsed JSON to the backend; must throw if it is rejected. */
  onLoad: (payload: unknown) => Promise<unknown>;
}

/**
 * File picker that reads a scenario JSON and sends it to the backend.
 *
 * The user picks the file from the UI (no fixed paths, as the project
 * statement requires). Parse errors and backend validation errors are shown
 * below the picker; on success the summary of the loaded scenario is shown.
 *
 * @param props.summary Current scenario summary.
 * @param props.onLoad Load action provided by the page.
 */
export function ScenarioLoader({ summary, onLoad }: ScenarioLoaderProps) {
  const [fileName, setFileName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  /**
   * Read the chosen file, parse it and send it.
   *
   * @param event Change event of the file input.
   */
  async function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;

    setFileName(file.name);
    setError(null);
    setIsLoading(true);

    try {
      let payload: unknown;
      try {
        payload = JSON.parse(await file.text());
      } catch {
        throw new Error("El archivo no contiene JSON válido.");
      }
      await onLoad(payload);
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
        className="field-control block text-sm text-slate-300 file:mr-3 file:border-0 file:bg-indigo-500 file:px-3 file:py-2 file:text-sm file:font-semibold file:text-white"
      />
      {fileName && <p className="text-xs text-slate-500">Archivo seleccionado: {fileName}</p>}
      {error && (
        <Notice tone="error">{`No se cargó el escenario. ${error}`}</Notice>
      )}
      {summary && !error && (
        <div className="rounded-lg border border-emerald-800 bg-emerald-950/30 p-3 text-sm text-emerald-200">
          <p className="font-semibold">{summary.name}</p>
          <p className="mt-1 text-xs text-emerald-300/80">
            GE: {summary.ge_vertex_count} vértices y {summary.ge_edge_count} aristas · base {summary.base_id}
          </p>
          <p className="text-xs text-emerald-300/80">
            GM: {summary.gm_vertex_count} vértices y {summary.gm_edge_count} corredores
          </p>
          <p className="text-xs text-emerald-300/80">
            Ruta más rápida {summary.shortest_maze_route.join(" → ")} ({formatSeconds(summary.shortest_maze_time)})
          </p>
        </div>
      )}
    </div>
  );
}
