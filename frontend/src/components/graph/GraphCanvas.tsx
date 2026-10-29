import { useEffect, useRef } from "react";
import * as d3 from "d3";
import type { Edge, Vertex } from "../../types/graph";

interface GraphCanvasProps {
  vertices: Vertex[];
  edges: Edge[];
  selectedVertexId: number | null;
  onSelectVertex: (vertex: Vertex) => void;
}

interface SimNode extends d3.SimulationNodeDatum {
  name: number;
  available: boolean;
}

interface SimLink extends d3.SimulationLinkDatum<SimNode> {
  source: number | SimNode;
  target: number | SimNode;
  weight: number;
}

export function GraphCanvas({
  vertices,
  edges,
  selectedVertexId,
  onSelectVertex,
}: GraphCanvasProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const svgRef = useRef<SVGSVGElement>(null);
  const onSelectRef = useRef(onSelectVertex);

  useEffect(() => {
    onSelectRef.current = onSelectVertex;
  }, [onSelectVertex]);

  useEffect(() => {
    const container = containerRef.current;
    const svgElement = svgRef.current;
    if (!container || !svgElement) return;

    const svg = d3.select(svgElement);
    svg.selectAll("*").remove();

    const { width, height } = container.getBoundingClientRect();
    if (!width || !height || vertices.length === 0) return;

    const nodes: SimNode[] = vertices.map((vertex) => ({
      name: vertex.name,
      available: vertex.available,
    }));
    const links: SimLink[] = edges.map((edge) => ({
      source: edge.source,
      target: edge.target,
      weight: edge.weight,
    }));

    const root = svg.attr("viewBox", `0 0 ${width} ${height}`);
    root
      .append("defs")
      .append("marker")
      .attr("id", "graph-arrow")
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 25)
      .attr("refY", 0)
      .attr("markerWidth", 6)
      .attr("markerHeight", 6)
      .attr("orient", "auto")
      .append("path")
      .attr("d", "M0,-5L10,0L0,5")
      .attr("fill", "#64748b");
    const link = root
      .append("g")
      .selectAll<SVGLineElement, SimLink>("line")
      .data(links)
      .join("line")
      .attr("class", "graph-link")
      .attr("marker-end", "url(#graph-arrow)");
    const linkLabels = root
      .append("g")
      .selectAll<SVGTextElement, SimLink>("text")
      .data(links)
      .join("text")
      .attr("class", "graph-link-label")
      .attr("text-anchor", "middle")
      .text((edge) => edge.weight);
    const node = root
      .append("g")
      .selectAll<SVGGElement, SimNode>("g")
      .data(nodes, (datum) => datum.name)
      .join("g")
      .attr("class", (datum) =>
        datum.name === selectedVertexId ? "graph-node is-selected" : "graph-node",
      )
      .attr("role", "button")
      .attr("tabindex", 0)
      .attr("aria-label", (datum) => `Seleccionar vértice ${datum.name}`)
      .on("click", (_event, datum) => {
        const selected = vertices.find((vertex) => vertex.name === datum.name);
        if (selected) onSelectRef.current(selected);
      })
      .on("keydown", (event, datum) => {
        if (event.key !== "Enter" && event.key !== " ") return;
        event.preventDefault();
        const selected = vertices.find((vertex) => vertex.name === datum.name);
        if (selected) onSelectRef.current(selected);
      });

    node
      .append("circle")
      .attr("r", 22)
      .attr("stroke", (datum) => (datum.available ? null : "#f87171"));
    node
      .append("text")
      .text((datum) => datum.name);

    const simulation = d3
      .forceSimulation<SimNode>(nodes)
      .force(
        "link",
        d3.forceLink<SimNode, SimLink>(links).id((datum) => datum.name).distance(125),
      )
      .force("charge", d3.forceManyBody().strength(-420))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collide", d3.forceCollide(42))
      .on("tick", () => {
        link
          .attr("x1", (datum) => (datum.source as SimNode).x ?? 0)
          .attr("y1", (datum) => (datum.source as SimNode).y ?? 0)
          .attr("x2", (datum) => (datum.target as SimNode).x ?? 0)
          .attr("y2", (datum) => (datum.target as SimNode).y ?? 0);
        linkLabels
          .attr(
            "x",
            (datum) =>
              (((datum.source as SimNode).x ?? 0) + ((datum.target as SimNode).x ?? 0)) /
              2,
          )
          .attr(
            "y",
            (datum) =>
              (((datum.source as SimNode).y ?? 0) + ((datum.target as SimNode).y ?? 0)) /
              2,
          );
        node.attr("transform", (datum) => `translate(${datum.x ?? 0},${datum.y ?? 0})`);
      });

    node.call(
      d3
        .drag<SVGGElement, SimNode>()
        .on("start", (event, datum) => {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          datum.fx = datum.x;
          datum.fy = datum.y;
        })
        .on("drag", (event, datum) => {
          datum.fx = event.x;
          datum.fy = event.y;
        })
        .on("end", (event, datum) => {
          if (!event.active) simulation.alphaTarget(0);
          datum.fx = null;
          datum.fy = null;
        }),
    );

    const observer = new ResizeObserver(() => {
      const bounds = container.getBoundingClientRect();
      if (!bounds.width || !bounds.height) return;
      svg.attr("viewBox", `0 0 ${bounds.width} ${bounds.height}`);
      simulation.force("center", d3.forceCenter(bounds.width / 2, bounds.height / 2));
      simulation.alpha(0.4).restart();
    });
    observer.observe(container);

    return () => {
      observer.disconnect();
      simulation.stop();
    };
  }, [edges, selectedVertexId, vertices]);

  return (
    <div ref={containerRef} className="graph-grid h-[28rem] w-full overflow-hidden rounded-xl">
      <svg
        ref={svgRef}
        className="h-full w-full"
        role="img"
        aria-label="Grafo dirigido. Selecciona un vértice para ver sus detalles."
      />
    </div>
  );
}
