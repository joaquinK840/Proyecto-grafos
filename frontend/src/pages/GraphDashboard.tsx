import { useMemo, useState } from "react";
import { FileJson, Mountain, Route, Timer } from "lucide-react";
import { ScenarioLoader } from "../components/forms/ScenarioLoader";
import { EdgeList } from "../components/graph/EdgeList";
import { GraphCanvas } from "../components/graph/GraphCanvas";
import { GraphLegend } from "../components/graph/GraphLegend";
import { GraphSelector } from "../components/graph/GraphSelector";
import { TraversalPanel } from "../components/graph/TraversalPanel";
import { VertexDetails } from "../components/graph/VertexDetails";
import { AppHeader } from "../components/ui/AppHeader";
import { Notice } from "../components/ui/Notice";
import { Panel } from "../components/ui/Panel";
import { StatCard } from "../components/ui/StatCard";
import { useScenario } from "../hooks/useScenario";
import { useScenarioGraphs } from "../hooks/useScenarioGraphs";
import { buildElevatedView } from "../presentation/elevatedGraphView";
import { formatSeconds } from "../presentation/formatters";
import { buildMazeView } from "../presentation/mazeGraphView";
import type { GraphKind } from "../types/graph";

/** Traversal result together with the graph it belongs to. */
interface TraversalState {
  kind: GraphKind;
  visitOrder: string[];
}

/**
 * Main page: loads a scenario and lets the user inspect GE and GM.
 *
 * It only composes: data comes from the hooks, the GE/GM specific
 * presentation from the adapters, and drawing from generic components.
 * Local state: which graph is shown, the selected vertex, the last
 * traversal and whether edge labels are visible.
 */
export function GraphDashboard() {
  const scenario = useScenario();
  const { graphs, isLoading: graphsLoading, error: graphsError } = useScenarioGraphs(
    scenario.summary,
  );
  const [kind, setKind] = useState<GraphKind>("ge");
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [traversal, setTraversal] = useState<TraversalState | null>(null);
  const [showLabels, setShowLabels] = useState(true);

  const summary = scenario.summary;
  const view = useMemo(() => {
    if (!graphs || !summary) return null;
    return kind === "ge"
      ? buildElevatedView(graphs.ge)
      : buildMazeView(graphs.gm, summary.shortest_maze_route_edges);
  }, [graphs, kind, summary]);

  const detail = view && selectedId ? view.describeVertex(selectedId) : null;
  const visitOrder = traversal?.kind === kind ? traversal.visitOrder : null;
  const error = scenario.error ?? graphsError;

  /**
   * Show another graph and clear the selection of the previous one.
   *
   * @param next Graph to show.
   */
  function changeKind(next: GraphKind) {
    setKind(next);
    setSelectedId(null);
  }

  /**
   * Load a scenario and reset everything that referred to the old one.
   *
   * @param payload Parsed scenario JSON.
   */
  async function loadScenario(payload: unknown) {
    await scenario.load(payload);
    setSelectedId(null);
    setTraversal(null);
  }

  return (
    <main className="app-shell">
      <div className="mx-auto max-w-[1500px] space-y-6 px-4 py-5 sm:px-6 lg:px-8 lg:py-7">
        <AppHeader
          isLoading={scenario.isLoading || graphsLoading}
          onRefresh={() => void scenario.refresh()}
        />

        <section className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard
            label="Escenario"
            value={summary?.name ?? "—"}
            detail={summary ? "Cargado en el servidor" : "Sin escenario cargado"}
            icon={<FileJson size={18} />}
            accent="indigo"
          />
          <StatCard
            label="Grafo elevado GE"
            value={summary ? `${summary.ge_vertex_count} · ${summary.ge_edge_count}` : "—"}
            detail={summary ? `Vértices · aristas · base ${summary.base_id}` : "Posiciones y puentes"}
            icon={<Mountain size={18} />}
            accent="amber"
          />
          <StatCard
            label="Laberinto GM"
            value={summary ? `${summary.gm_vertex_count} · ${summary.gm_edge_count}` : "—"}
            detail={summary ? `Vértices · corredores · ${summary.entry_id} → ${summary.exit_id}` : "Corredores del convoy"}
            icon={<Route size={18} />}
            accent="cyan"
          />
          <StatCard
            label="Ruta más rápida GM"
            value={summary ? formatSeconds(summary.shortest_maze_time) : "—"}
            detail={summary ? summary.shortest_maze_route.join(" → ") : "Entrada → salida"}
            icon={<Timer size={18} />}
            accent="emerald"
          />
        </section>

        {error && <Notice tone="error">{error}</Notice>}

        <div className="grid items-start gap-5 xl:grid-cols-[minmax(0,1fr)_340px]">
          <div className="space-y-5">
            <GraphSelector
              value={kind}
              onChange={changeKind}
              counts={{
                ge: summary?.ge_vertex_count ?? 0,
                gm: summary?.gm_vertex_count ?? 0,
              }}
            />

            <Panel
              title={view?.title ?? (kind === "ge" ? "Grafo elevado GE" : "Laberinto GM")}
              description={view?.description ?? "Carga un escenario para visualizar los grafos."}
              action={
                <label className="flex shrink-0 items-center gap-2 text-xs text-slate-400">
                  <input
                    type="checkbox"
                    checked={showLabels}
                    onChange={(event) => setShowLabels(event.target.checked)}
                    className="accent-indigo-500"
                  />
                  Etiquetas
                </label>
              }
            >
              {view ? (
                <>
                  <GraphCanvas
                    nodes={view.nodes}
                    links={view.links}
                    selectedId={selectedId}
                    visitOrder={visitOrder ?? []}
                    showLabels={showLabels}
                    onSelect={setSelectedId}
                  />
                  <GraphLegend items={view.legend} />
                </>
              ) : (
                <div className="graph-grid flex h-[30rem] flex-col items-center justify-center gap-3 rounded-xl text-center">
                  <FileJson size={34} className="text-indigo-300" />
                  <div>
                    <p className="font-medium text-slate-200">
                      {scenario.isLoading || graphsLoading ? "Cargando…" : "Todavía no hay escenario"}
                    </p>
                    <p className="mt-1 text-sm text-slate-400">
                      Selecciona un archivo JSON en el panel «Escenario» para construir GE y GM.
                    </p>
                  </div>
                </div>
              )}
            </Panel>

            {view && (
              <div className="grid items-start gap-5 lg:grid-cols-2">
                <VertexDetails detail={detail} onSelect={setSelectedId} />
                <EdgeList rows={view.edgeRows} />
              </div>
            )}
          </div>

          <aside className="space-y-4">
            <Panel title="Escenario" description="Carga la configuración de las redes GE y GM.">
              <ScenarioLoader summary={summary} onLoad={loadScenario} />
            </Panel>
            <Panel
              title="Exploración"
              description={`Recorridos sobre ${kind === "ge" ? "GE" : "GM"} desde una posición inicial.`}
            >
              <TraversalPanel
                key={kind}
                kind={kind}
                vertexIds={view?.vertexIds ?? []}
                visitOrder={visitOrder}
                onResult={(order) => setTraversal(order ? { kind, visitOrder: order } : null)}
              />
            </Panel>
          </aside>
        </div>
      </div>
    </main>
  );
}
