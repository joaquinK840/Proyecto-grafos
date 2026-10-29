import { useState } from "react";
import { CircleDot, GitBranch, RefreshCw, Waypoints } from "lucide-react";
import { CreateEdgeForm } from "../components/forms/CreateEdgeForm";
import { CreateVertexForm } from "../components/forms/CreateVertexForm";
import { GraphCanvas } from "../components/graph/GraphCanvas";
import { TraversalPanel } from "../components/graph/TraversalPanel";
import { VertexDetails } from "../components/graph/VertexDetails";
import { Notice } from "../components/ui/Notice";
import { Panel } from "../components/ui/Panel";
import { useGraph } from "../hooks/useGraph";
import type { Vertex } from "../types/graph";

export function GraphDashboard() {
  const { vertices, edges, isLoading, error, refresh, createVertex, createEdge } =
    useGraph();
  const [selectedVertex, setSelectedVertex] = useState<Vertex | null>(null);

  const selected = selectedVertex
    ? vertices.find((vertex) => vertex.name === selectedVertex.name) ?? null
    : null;

  return (
    <main className="min-h-screen bg-[radial-gradient(ellipse_at_top,_#1e1b4b_0%,_#0b1020_45%)] px-4 py-6 text-slate-100 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-[1500px] space-y-6">
        <header className="flex flex-col justify-between gap-4 border-b border-slate-800 pb-5 sm:flex-row sm:items-center">
          <div>
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-indigo-500/15 p-2.5 text-indigo-300">
                <GitBranch size={23} />
              </div>
              <div>
                <h1 className="text-2xl font-bold tracking-tight text-white sm:text-3xl">
                  Graph Studio
                </h1>
                <p className="mt-1 text-sm text-slate-400">
                  Administra y explora tu grafo dirigido.
                </p>
              </div>
            </div>
          </div>
          <button
            type="button"
            onClick={() => void refresh()}
            disabled={isLoading}
            className="inline-flex items-center justify-center gap-2 self-start rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-300 transition hover:border-slate-500 hover:bg-slate-800 disabled:opacity-50 sm:self-auto"
          >
            <RefreshCw size={15} className={isLoading ? "animate-spin" : ""} />
            Actualizar
          </button>
        </header>

        <section className="grid grid-cols-2 gap-3 sm:grid-cols-3">
          <StatCard label="Vértices" value={vertices.length} icon={<CircleDot size={18} />} />
          <StatCard label="Aristas" value={edges.length} icon={<Waypoints size={18} />} />
          <div className="col-span-2 sm:col-span-1">
            <StatCard
              label="Tipo de grafo"
              value="Dirigido"
              icon={<GitBranch size={18} />}
              compact
            />
          </div>
        </section>

        {error && (
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
            <div className="flex-1"><Notice tone="error">{error}</Notice></div>
            <button
              type="button"
              onClick={() => void refresh()}
              className="rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-200 hover:bg-slate-800"
            >
              Reintentar
            </button>
          </div>
        )}

        <div className="grid items-start gap-5 xl:grid-cols-[minmax(0,1fr)_340px]">
          <div className="space-y-5">
            <Panel
              title="Visualización del grafo"
              description="Arrastra los nodos para acomodarlos. Selecciona uno para ver sus detalles."
              action={
                <span className="hidden rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-300 sm:inline-flex">
                  {vertices.length} nodos · {edges.length} conexiones
                </span>
              }
            >
              {isLoading && !vertices.length ? (
                <div className="graph-grid flex h-[28rem] items-center justify-center rounded-xl text-sm text-slate-400">
                  Cargando grafo…
                </div>
              ) : vertices.length ? (
                <GraphCanvas
                  vertices={vertices}
                  edges={edges}
                  selectedVertexId={selected?.name ?? null}
                  onSelectVertex={setSelectedVertex}
                />
              ) : (
                <div className="graph-grid flex h-[28rem] flex-col items-center justify-center gap-3 rounded-xl text-center">
                  <CircleDot size={34} className="text-indigo-300" />
                  <div>
                    <p className="font-medium text-slate-200">Todavía no hay vértices</p>
                    <p className="mt-1 text-sm text-slate-400">
                      Crea un vértice para comenzar a construir el grafo.
                    </p>
                  </div>
                </div>
              )}
            </Panel>
            <VertexDetails vertex={selected} edges={edges} />
          </div>

          <aside className="space-y-5">
            <Panel title="Añadir vértice">
              <CreateVertexForm onCreate={(name) => createVertex({ name })} />
            </Panel>
            <Panel title="Añadir arista" description="Crea una conexión dirigida con peso.">
              <CreateEdgeForm vertices={vertices} onCreate={createEdge} />
            </Panel>
            <Panel title="Recorridos" description="Explora el grafo desde un vértice inicial.">
              <TraversalPanel vertices={vertices} />
            </Panel>
          </aside>
        </div>
      </div>
    </main>
  );
}

interface StatCardProps {
  label: string;
  value: string | number;
  icon: React.ReactNode;
  compact?: boolean;
}

function StatCard({ label, value, icon, compact = false }: StatCardProps) {
  return (
    <div className="flex items-center gap-3 rounded-2xl border border-slate-800 bg-slate-900/70 p-4">
      <div className="rounded-lg bg-indigo-500/10 p-2 text-indigo-300">{icon}</div>
      <div>
        <p className="text-xs text-slate-400">{label}</p>
        <p className={`mt-0.5 font-semibold text-slate-100 ${compact ? "text-base" : "text-xl"}`}>
          {value}
        </p>
      </div>
    </div>
  );
}
