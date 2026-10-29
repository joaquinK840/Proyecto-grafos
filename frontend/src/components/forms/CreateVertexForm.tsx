import { useState, type FormEvent } from "react";

interface CreateVertexFormProps {
  onCreate: (name: number) => Promise<void>;
}

export function CreateVertexForm({ onCreate }: CreateVertexFormProps) {
  const [name, setName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const parsedName = Number(name);
    if (!Number.isInteger(parsedName)) {
      setError("Ingresa un identificador entero.");
      return;
    }

    setError(null);
    setIsSaving(true);
    try {
      await onCreate(parsedName);
      setName("");
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "No se pudo crear el vértice.");
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <label htmlFor="vertex-name" className="block text-sm font-medium text-slate-300">
        Identificador
      </label>
      <div className="flex gap-2">
        <input
          id="vertex-name"
          type="number"
          step="1"
          required
          value={name}
          onChange={(event) => setName(event.target.value)}
          placeholder="Ej. 12"
          className="min-w-0 flex-1 rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white placeholder:text-slate-600"
        />
        <button
          type="submit"
          disabled={isSaving}
          className="rounded-lg bg-indigo-500 px-4 py-2 text-sm font-semibold text-white transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isSaving ? "Guardando…" : "Crear"}
        </button>
      </div>
      {error && <p role="alert" className="text-sm text-rose-300">{error}</p>}
    </form>
  );
}
