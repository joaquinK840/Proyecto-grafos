import type { LegendItem } from "../../types/graphView";

interface GraphLegendProps {
  items: LegendItem[];
}

/**
 * Legend with the meaning of node colors and edge styles.
 *
 * @param props.items Entries produced by the graph adapter; node entries are
 *        drawn as dots and link entries as short lines, using the same CSS
 *        classes as the canvas so they always match.
 */
export function GraphLegend({ items }: GraphLegendProps) {
  return (
    <ul className="mt-3 flex flex-wrap gap-x-4 gap-y-2 text-xs text-slate-400">
      {items.map((item) => (
        <li key={`${item.kind}-${item.tone}`} className="flex items-center gap-2">
          <svg width="22" height="14" aria-hidden="true">
            {item.kind === "node" ? (
              <g className={`graph-node node-${item.tone}`}>
                <circle cx="11" cy="7" r="5.5" />
              </g>
            ) : (
              <line
                className={legendLinkClass(item.tone)}
                x1="1"
                y1="7"
                x2="21"
                y2="7"
              />
            )}
          </svg>
          {item.label}
        </li>
      ))}
    </ul>
  );
}

/**
 * CSS classes for a link entry of the legend.
 *
 * @param tone Link tone, or the special "unavailable" / "route" states.
 * @returns Classes equivalent to the ones the canvas uses.
 */
function legendLinkClass(tone: string): string {
  if (tone === "unavailable") return "graph-link link-path is-unavailable";
  if (tone === "route") return "graph-link link-corridor is-route";
  return `graph-link link-${tone}`;
}
