import { useState, type FormEvent } from "react";
import type { EdgeInput, Vertex } from "../../types/graph";

interface CreateEdgeFormProps {
  vertices: Vertex[];
  onCreate: (edge: EdgeInput) => Promise<void>;
}

export function CreateEdgeForm({ vertices, onCreate }: CreateEdgeFormProps) {
  const [source, setSource] = useState("");
  const [target, setTarget] = useState("");
  const [weight, setWeight] = useState("1");
  const [error, setError] = useState<string | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsSaving(true);
    try {
      await onCreate({
        source: Number(source),
        target: Number(target),
        weight: Number(weight),
      });
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "No se pudo crear la arista.");
    } finally {
      setIsSaving(false);
    }
  }

  const selectClass =
    "w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-200";

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <label className="block text-sm font-medium text-slate-300">
        Desde
        <select
          required
          value={source}
          onChange={(event) => setSource(event.target.value)}
          className={`mt-1 ${selectClass}`}
          disabled={!vertices.length}
        >
          <option value="" disabled>Elige origen</option>
          {vertices.map((vertex) => (
            <option key={vertex.name} value={vertex.name}>Vértice {vertex.name}</option>
          ))}
        </select>
      </label>

      <label className="block text-sm font-medium text-slate-300">
        Hacia
        <select
          required
          value={target}
          onChange={(event) => setTarget(event.target.value)}
          className={`mt-1 ${selectClass}`}
          disabled={!vertices.length}
        >
          <option value="" disabled>Elige destino</option>
          {vertices.map((vertex) => (
            <option key={vertex.name} value={vertex.name}>Vértice {vertex.name}</option>
          ))}
        </select>
      </label>

      <label className="block text-sm font-medium text-slate-300">
        Peso
        <input
          type="number"
          step="1"
          required
          value={weight}
          onChange={(event) => setWeight(event.target.value)}
          className={`mt-1 ${selectClass}`}
        />
      </label>

      <button
        type="submit"
        disabled={isSaving || vertices.length < 2}
        className="w-full rounded-lg border border-indigo-400/40 bg-indigo-500/10 px-4 py-2 text-sm font-semibold text-indigo-200 transition hover:bg-indigo-500/20 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {isSaving ? "Conectando…" : "Crear conexión"}
      </button>
      {vertices.length < 2 && (
        <p className="text-xs text-slate-500">Crea al menos dos vértices para conectarlos.</p>
      )}
      {error && <p role="alert" className="text-sm text-rose-300">{error}</p>}
    </form>
  );
}
