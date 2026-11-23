import type { EdgeRow } from "../../types/graphView";
import { Panel } from "../ui/Panel";

interface EdgeListProps {
  rows: EdgeRow[];
}

/**
 * Panel listing every edge of the graph with its data and state.
 *
 * @param props.rows Rows produced by the graph adapter (endpoints, type,
 *        metrics, availability and route membership).
 */
export function EdgeList({ rows }: EdgeListProps) {
  return (
    <Panel title="Aristas" description={`${rows.length} conexiones no dirigidas.`}>
      {rows.length ? (
        <ul className="max-h-80 space-y-2 overflow-y-auto pr-1">
          {rows.map((row) => (
            <li
              key={row.id}
              className={`edge-row ${row.highlighted ? "is-route" : ""} ${
                row.available ? "" : "is-unavailable"
              }`}
            >
              <div className="flex items-center justify-between gap-2">
                <span className="font-medium text-slate-100">
                  {row.id} <span className="text-slate-400">· {row.endpoints}</span>
                </span>
                <span className={`status-pill ${row.available ? "is-ok" : "is-off"}`}>
                  {row.statusLabel}
                </span>
              </div>
              <p className="mt-1 text-xs text-slate-400">
                {row.typeLabel} · {row.metrics}
              </p>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-sm text-slate-500">El grafo no tiene aristas.</p>
      )}
    </Panel>
  );
}
