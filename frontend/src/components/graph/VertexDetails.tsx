import { CircleDot, Waypoints } from "lucide-react";
import type { VertexDetail } from "../../types/graphView";
import { Panel } from "../ui/Panel";

interface VertexDetailsProps {
  detail: VertexDetail | null;
  onSelect: (vertexId: string) => void;
}

/**
 * Panel with the data of the selected vertex and its incident edges.
 *
 * Graph-agnostic: the adapter decides which fields and connection
 * summaries to show for GE or GM.
 *
 * @param props.detail Details of the selected vertex, or null.
 * @param props.onSelect Called when a neighbor is clicked, to jump to it.
 */
export function VertexDetails({ detail, onSelect }: VertexDetailsProps) {
  return (
    <Panel
      title="Detalle del vértice"
      description="Selecciona un nodo de la gráfica para inspeccionar sus datos."
    >
      {!detail ? (
        <div className="flex min-h-44 flex-col items-center justify-center gap-3 text-center text-sm text-slate-400">
          <CircleDot size={28} className="text-indigo-300" />
          <p>Sin vértice seleccionado</p>
        </div>
      ) : (
        <div className="space-y-5">
          <div className="flex items-center justify-between gap-3 rounded-xl bg-slate-800/70 p-4">
            <div className="min-w-0">
              <p className="text-xs uppercase tracking-wider text-slate-400">Identificador</p>
              <p className="mt-1 truncate text-2xl font-bold text-white">{detail.id}</p>
            </div>
            <span className={`tone-badge tone-${detail.tone}`}>{detail.typeLabel}</span>
          </div>

          <dl className="grid grid-cols-3 gap-3">
            {detail.fields.map((field) => (
              <div key={field.label} className="rounded-xl border border-slate-800 p-3">
                <dt className="text-xs text-slate-400">{field.label}</dt>
                <dd className="mt-1 text-sm font-semibold text-slate-100">{field.value}</dd>
              </div>
            ))}
          </dl>

          <div>
            <div className="mb-2 flex items-center gap-2 text-sm font-medium text-slate-200">
              <Waypoints size={16} className="text-indigo-300" />
              Conexiones
            </div>
            {detail.connections.length ? (
              <ul className="space-y-2">
                {detail.connections.map((connection) => (
                  <li key={connection.edgeId}>
                    <button
                      type="button"
                      onClick={() => onSelect(connection.neighborId)}
                      className={`connection-item ${connection.highlighted ? "is-route" : ""} ${
                        connection.available ? "" : "is-unavailable"
                      }`}
                    >
                      <span className="font-medium text-slate-100">
                        {connection.edgeId} → {connection.neighborId}
                      </span>
                      <span className="text-xs text-slate-400">{connection.summary}</span>
                    </button>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-slate-500">No tiene conexiones.</p>
            )}
          </div>
        </div>
      )}
    </Panel>
  );
}
