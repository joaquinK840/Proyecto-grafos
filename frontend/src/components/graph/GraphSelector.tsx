import { Mountain, Route } from "lucide-react";
import type { GraphKind } from "../../types/graph";

interface GraphSelectorProps {
  value: GraphKind;
  onChange: (kind: GraphKind) => void;
  /** Number of vertices of each graph, shown next to its name. */
  counts: Record<GraphKind, number>;
}

const OPTIONS: { kind: GraphKind; label: string; icon: typeof Mountain }[] = [
  { kind: "ge", label: "Grafo elevado GE", icon: Mountain },
  { kind: "gm", label: "Laberinto GM", icon: Route },
];

/**
 * Tabs to switch the view between GE and GM.
 *
 * @param props.value Graph currently shown.
 * @param props.onChange Called with the selected graph.
 * @param props.counts Vertex count of each graph.
 */
export function GraphSelector({ value, onChange, counts }: GraphSelectorProps) {
  return (
    <div role="tablist" aria-label="Grafo a visualizar" className="graph-tabs">
      {OPTIONS.map(({ kind, label, icon: Icon }) => (
        <button
          key={kind}
          type="button"
          role="tab"
          aria-selected={value === kind}
          onClick={() => onChange(kind)}
          className={`graph-tab ${value === kind ? "is-active" : ""}`}
        >
          <Icon size={15} />
          {label}
          <span className="graph-tab-count">{counts[kind]}</span>
        </button>
      ))}
    </div>
  );
}
