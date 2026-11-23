import type { EdgeGM, MazeGraphData, MazeVertexRole, VertexGM } from "../types/graph";
import type { GraphView, LegendItem, NodeTone, VertexDetail } from "../types/graphView";
import { incidentEdges, oppositeEnd } from "./edgeHelpers";
import { formatCoordinates, formatNumber, formatSeconds } from "./formatters";

/** Spanish label and color category of every GM role. */
const ROLE_STYLES: Record<MazeVertexRole, { label: string; tone: NodeTone }> = {
  entry: { label: "Entrada", tone: "entry" },
  exit: { label: "Salida", tone: "exit" },
  normal: { label: "Intersección", tone: "intersection" },
};

const LEGEND: LegendItem[] = [
  ...Object.values(ROLE_STYLES).map(
    ({ label, tone }): LegendItem => ({ kind: "node", tone, label }),
  ),
  { kind: "link", tone: "corridor", label: "Corredor" },
  { kind: "link", tone: "route", label: "Ruta más rápida" },
  { kind: "link", tone: "unavailable", label: "No disponible" },
];

/**
 * Describe the length, speed and travel time of a corridor.
 *
 * @param edge GM corridor.
 * @returns For example `l 10 · v 2 · t 5 s`.
 */
function describeCorridor(edge: EdgeGM): string {
  return `l ${formatNumber(edge.length)} · v ${formatNumber(edge.speed)} · t ${formatSeconds(edge.travel_time)}`;
}

/**
 * Build the details of a GM vertex.
 *
 * @param vertex Vertex to describe.
 * @param edges Every GM corridor.
 * @param route Edge ids of the fastest route.
 * @returns Fields (coordinates, degree, route membership) and incident corridors.
 */
function describeVertex(vertex: VertexGM, edges: EdgeGM[], route: Set<string>): VertexDetail {
  const style = ROLE_STYLES[vertex.role];
  const incident = incidentEdges(edges, vertex.id);
  return {
    id: vertex.id,
    typeLabel: style.label,
    tone: style.tone,
    fields: [
      { label: "Coordenadas", value: formatCoordinates(vertex.x, vertex.y) },
      { label: "Grado", value: formatNumber(incident.length) },
      {
        label: "En ruta más rápida",
        value: incident.some((edge) => route.has(edge.id)) ? "Sí" : "No",
      },
    ],
    connections: incident.map((edge) => ({
      edgeId: edge.id,
      neighborId: oppositeEnd(edge, vertex.id),
      summary: describeCorridor(edge),
      available: edge.available,
      highlighted: route.has(edge.id),
    })),
  };
}

/**
 * Translate the GM API data into the generic graph view.
 *
 * @param data Vertices and corridors of GM.
 * @param routeEdgeIds Edge ids of the fastest entry→exit route, to highlight them.
 * @returns View with entry/exit/intersections, corridor travel times and the route.
 */
export function buildMazeView(data: MazeGraphData, routeEdgeIds: string[]): GraphView {
  const byId = new Map(data.vertices.map((vertex) => [vertex.id, vertex]));
  const route = new Set(routeEdgeIds);

  return {
    kind: "gm",
    title: "Laberinto GM",
    description: "Corredores del convoy. Cada corredor tarda t(e) = l(e) / v(e).",
    nodes: data.vertices.map((vertex) => ({
      id: vertex.id,
      x: vertex.x,
      y: vertex.y,
      tone: ROLE_STYLES[vertex.role].tone,
      tooltip: `${vertex.id} · ${ROLE_STYLES[vertex.role].label}`,
    })),
    links: data.edges.map((edge) => ({
      id: edge.id,
      source: edge.v1,
      target: edge.v2,
      tone: "corridor",
      label: `t ${formatSeconds(edge.travel_time)}`,
      available: edge.available,
      highlighted: route.has(edge.id),
    })),
    legend: LEGEND,
    edgeRows: data.edges.map((edge) => ({
      id: edge.id,
      endpoints: `${edge.v1} — ${edge.v2}`,
      typeLabel: route.has(edge.id) ? "Corredor · ruta" : "Corredor",
      metrics: describeCorridor(edge),
      statusLabel: edge.available ? "Disponible" : "Inhabilitado",
      available: edge.available,
      highlighted: route.has(edge.id),
    })),
    vertexIds: data.vertices.map((vertex) => vertex.id),
    describeVertex: (vertexId) => {
      const vertex = byId.get(vertexId);
      return vertex ? describeVertex(vertex, data.edges, route) : null;
    },
  };
}
