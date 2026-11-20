import { useState } from "react";
import { CircleDot, GitBranch, Waypoints } from "lucide-react";
import { CreateEdgeForm } from "../components/forms/CreateEdgeForm";
import { CreateVertexForm } from "../components/forms/CreateVertexForm";
import { ScenarioLoader } from "../components/forms/ScenarioLoader";
import { GraphCanvas } from "../components/graph/GraphCanvas";
import { TraversalPanel } from "../components/graph/TraversalPanel";
import { VertexDetails } from "../components/graph/VertexDetails";
import { Notice } from "../components/ui/Notice";
import { Panel } from "../components/ui/Panel";
import { AppHeader } from "../components/ui/AppHeader";
import { StatCard } from "../components/ui/StatCard";
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
    <main className="app-shell">
      <div className="mx-auto max-w-[1500px] space-y-6 px-4 py-5 sm:px-6 lg:px-8 lg:py-7">
        <AppHeader isLoading={isLoading} onRefresh={() => void refresh()} />

        <section className="grid gap-3 sm:grid-cols-3">
          <StatCard
            label="Redes activas"
            value={vertices.length ? 2 : 0}
            detail={vertices.length ? "GE elevada · GM laberinto" : "Sin escenario cargado"}
            icon={<GitBranch size={18} />}
            accent="indigo"
          />
          <StatCard
            label="Posiciones"
            value={vertices.length}
            detail="Vértices disponibles"
            icon={<CircleDot size={18} />}
            accent="cyan"
          />
          <StatCard
            label="Conexiones"
            value={edges.length}
            detail="Aristas dirigidas"
            icon={<Waypoints size={18} />}
            accent="emerald"
          />
        </section>

        {error && (
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
            <div className="flex-1"><Notice tone="error">{error}</Notice></div>
            <button
              type="button"
              onClick={() => void refresh()}
              className="button-secondary"
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

          <aside className="space-y-4">
            <Panel title="Escenario" description="Carga la configuración de las redes GE y GM.">
              <ScenarioLoader />
            </Panel>
            <Panel title="Nueva posición" description="Agrega un vértice al grafo operativo.">
              <CreateVertexForm onCreate={(name) => createVertex({ name })} />
            </Panel>
            <Panel title="Nueva conexión" description="Crea una arista dirigida con peso.">
              <CreateEdgeForm vertices={vertices} onCreate={createEdge} />
            </Panel>
            <Panel title="Exploración" description="Ejecuta recorridos desde una posición inicial.">
              <TraversalPanel vertices={vertices} />
            </Panel>
          </aside>
        </div>
      </div>
    </main>
  );
}

