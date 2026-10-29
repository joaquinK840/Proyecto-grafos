import { ArrowLeft, ArrowRight, CircleDot, Waypoints } from "lucide-react";
import type { Edge, Vertex } from "../../types/graph";
import { Panel } from "../ui/Panel";

interface VertexDetailsProps {
  vertex: Vertex | null;
  edges: Edge[];
}

export function VertexDetails({ vertex, edges }: VertexDetailsProps) {
  const outgoingEdges = vertex
    ? edges.filter((edge) => edge.source === vertex.name)
    : [];
  const incomingEdges = vertex
    ? edges.filter((edge) => edge.target === vertex.name)
    : [];

  return (
    <Panel
      title="Detalle del vértice"
      description="Selecciona un nodo de la gráfica para inspeccionar sus datos."
    >
      {!vertex ? (
        <div className="flex min-h-44 flex-col items-center justify-center gap-3 text-center text-sm text-slate-400">
          <CircleDot size={28} className="text-indigo-300" />
          <p>Sin vértice seleccionado</p>
        </div>
      ) : (
        <div className="space-y-5">
          <div className="flex items-center justify-between rounded-xl bg-slate-800/70 p-4">
            <div>
              <p className="text-xs uppercase tracking-wider text-slate-400">Identificador</p>
              <p className="mt-1 text-2xl font-bold text-white">#{vertex.name}</p>
            </div>
            <span
              className={`rounded-full px-3 py-1 text-xs font-medium ${
                vertex.available
                  ? "bg-emerald-950 text-emerald-300"
                  : "bg-rose-950 text-rose-300"
              }`}
            >
              {vertex.available ? "Disponible" : "No disponible"}
            </span>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="rounded-xl border border-slate-800 p-3">
              <p className="text-xs text-slate-400">Grado de salida</p>
              <p className="mt-1 text-lg font-semibold text-slate-100">
                {outgoingEdges.length}
              </p>
            </div>
            <div className="rounded-xl border border-slate-800 p-3">
              <p className="text-xs text-slate-400">Grado de entrada</p>
              <p className="mt-1 text-lg font-semibold text-slate-100">
                {incomingEdges.length}
              </p>
            </div>
          </div>

          <ConnectionList
            title="Conexiones salientes"
            edges={outgoingEdges}
            emptyMessage="No tiene aristas salientes."
            direction="outgoing"
          />
          <ConnectionList
            title="Conexiones entrantes"
            edges={incomingEdges}
            emptyMessage="No tiene aristas entrantes."
            direction="incoming"
          />
        </div>
      )}
    </Panel>
  );
}

interface ConnectionListProps {
  title: string;
  edges: Edge[];
  emptyMessage: string;
  direction: "incoming" | "outgoing";
}

function ConnectionList({
  title,
  edges,
  emptyMessage,
  direction,
}: ConnectionListProps) {
  const Arrow = direction === "outgoing" ? ArrowRight : ArrowLeft;

  return (
    <div>
      <div className="mb-2 flex items-center gap-2 text-sm font-medium text-slate-200">
        <Waypoints size={16} className="text-indigo-300" />
        {title}
      </div>
      {edges.length ? (
        <ul className="space-y-2">
          {edges.map((edge, index) => (
            <li
              key={`${edge.source}-${edge.target}-${index}`}
              className="flex items-center justify-between rounded-lg bg-slate-800/60 px-3 py-2 text-sm"
            >
              <span className="flex items-center gap-2 text-slate-200">
                <span>#{edge.source}</span>
                <Arrow size={14} className="text-slate-500" />
                <span>#{edge.target}</span>
              </span>
              <span className="text-slate-400">peso {edge.weight}</span>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-sm text-slate-500">{emptyMessage}</p>
      )}
    </div>
  );
}
