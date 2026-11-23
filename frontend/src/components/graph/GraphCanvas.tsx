import { useMemo, useRef, type KeyboardEvent } from "react";
import { useElementSize } from "../../hooks/useElementSize";
import { projectToScreen } from "../../presentation/canvasLayout";
import type { CanvasLink, CanvasNode } from "../../types/graphView";

const NODE_RADIUS = 15;
const PADDING = 56;

interface GraphCanvasProps {
  nodes: CanvasNode[];
  links: CanvasLink[];
  selectedId: string | null;
  /** Ids in traversal order; each node shows its position as a badge. */
  visitOrder: string[];
  showLabels: boolean;
  onSelect: (vertexId: string) => void;
}

/**
 * Draw an undirected graph at the real coordinates of its vertices.
 *
 * It is graph-agnostic: colors come from the `tone` of nodes and links
 * (CSS classes), so the same component draws GE and GM.
 *
 * @param props.nodes Vertices to draw.
 * @param props.links Edges to draw (unavailable ones are dashed in red,
 *        highlighted ones are drawn thicker in green).
 * @param props.selectedId Vertex to highlight as selected.
 * @param props.visitOrder Traversal result to show as numbered badges.
 * @param props.showLabels Whether to draw the edge labels.
 * @param props.onSelect Called with the id of a clicked / activated vertex.
 */
export function GraphCanvas({
  nodes,
  links,
  selectedId,
  visitOrder,
  showLabels,
  onSelect,
}: GraphCanvasProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const { width, height } = useElementSize(containerRef);

  const positions = useMemo(
    () => projectToScreen(nodes, width, height, PADDING),
    [nodes, width, height],
  );
  const orderById = useMemo(
    () => new Map(visitOrder.map((id, index) => [id, index + 1])),
    [visitOrder],
  );

  /**
   * Activate a vertex with Enter or Space (keyboard accessibility).
   *
   * @param event Keyboard event on the node.
   * @param vertexId Node that received the event.
   */
  function handleKeyDown(event: KeyboardEvent<SVGGElement>, vertexId: string) {
    if (event.key !== "Enter" && event.key !== " ") return;
    event.preventDefault();
    onSelect(vertexId);
  }

  return (
    <div ref={containerRef} className="graph-grid h-[30rem] w-full overflow-hidden rounded-xl">
      {width > 0 && height > 0 && (
        <svg
          viewBox={`0 0 ${width} ${height}`}
          className="h-full w-full"
          role="group"
          aria-label="Grafo no dirigido dibujado en sus coordenadas. Selecciona un vértice para ver sus detalles."
        >
          <g>
            {links.map((link) => {
              const from = positions.get(link.source);
              const to = positions.get(link.target);
              if (!from || !to) return null;
              const classes = [
                "graph-link",
                `link-${link.tone}`,
                link.available ? "" : "is-unavailable",
                link.highlighted ? "is-route" : "",
              ].join(" ");
              return (
                <g key={link.id}>
                  <line className={classes} x1={from.x} y1={from.y} x2={to.x} y2={to.y}>
                    <title>{`${link.id}: ${link.label}`}</title>
                  </line>
                  {showLabels && (
                    <text
                      className="graph-link-label"
                      x={(from.x + to.x) / 2}
                      y={(from.y + to.y) / 2 - 6}
                      textAnchor="middle"
                    >
                      {link.label}
                    </text>
                  )}
                </g>
              );
            })}
          </g>

          <g>
            {nodes.map((node) => {
              const point = positions.get(node.id);
              if (!point) return null;
              const order = orderById.get(node.id);
              const classes = [
                "graph-node",
                `node-${node.tone}`,
                node.id === selectedId ? "is-selected" : "",
                order ? "is-visited" : "",
              ].join(" ");
              return (
                <g
                  key={node.id}
                  className={classes}
                  transform={`translate(${point.x},${point.y})`}
                  role="button"
                  tabIndex={0}
                  aria-label={`Seleccionar vértice ${node.tooltip}`}
                  aria-pressed={node.id === selectedId}
                  onClick={() => onSelect(node.id)}
                  onKeyDown={(event) => handleKeyDown(event, node.id)}
                >
                  <title>{node.tooltip}</title>
                  <circle r={NODE_RADIUS} />
                  <text className="graph-node-label" y={NODE_RADIUS + 14}>
                    {node.id}
                  </text>
                  {order && (
                    <g className="graph-node-order" transform={`translate(${NODE_RADIUS},${-NODE_RADIUS})`}>
                      <circle r={9} />
                      <text>{order}</text>
                    </g>
                  )}
                </g>
              );
            })}
          </g>
        </svg>
      )}
    </div>
  );
}
