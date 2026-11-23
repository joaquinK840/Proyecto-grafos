import type { EdgeGE, ElevatedGraphData, PositionType, VertexGE } from "../types/graph";
import type { GraphView, LegendItem, NodeTone, VertexDetail } from "../types/graphView";
import { incidentEdges, oppositeEnd } from "./edgeHelpers";
import { formatCoordinates, formatNumber, formatSeconds } from "./formatters";

/** Spanish label and color category of every GE position type. */
const POSITION_STYLES: Record<PositionType, { label: string; tone: NodeTone }> = {
  base: { label: "Base", tone: "base" },
  tower_candidate: { label: "Candidato a torre", tone: "tower" },
  transit: { label: "Tránsito", tone: "transit" },
  heliport: { label: "Helipuerto", tone: "heliport" },
};

const LEGEND: LegendItem[] = [
  ...Object.values(POSITION_STYLES).map(
    ({ label, tone }): LegendItem => ({ kind: "node", tone, label }),
  ),
  { kind: "link", tone: "path", label: "Camino" },
  { kind: "link", tone: "bridge", label: "Puente" },
  { kind: "link", tone: "unavailable", label: "No disponible" },
];

/**
 * Describe the transport times of a GE edge.
 *
 * @param edge GE edge.
 * @returns For example `pie 5 s · moto 2 s`.
 */
function describeTimes(edge: EdgeGE): string {
  return `pie ${formatSeconds(edge.foot_time)} · moto ${formatSeconds(edge.moto_time)}`;
}

/**
 * Describe the resistance of a bridge.
 *
 * @param edge GE edge.
 * @returns `R actual/máxima` for bridges, empty text for paths.
 */
function describeResistance(edge: EdgeGE): string {
  if (edge.connection_type !== "bridge") return "";
  return `R ${edge.current_resistance ?? 0}/${edge.max_resistance ?? 0}`;
}

/**
 * Human readable state of a GE edge.
 *
 * @param edge GE edge.
 * @returns "Destruido" for collapsed bridges, "Inhabilitada" if disabled, otherwise "Disponible".
 */
function describeStatus(edge: EdgeGE): string {
  if (edge.connection_type === "bridge" && edge.current_resistance === 0) return "Destruido";
  return edge.available ? "Disponible" : "Inhabilitada";
}

/**
 * Spanish name of the connection type.
 *
 * @param edge GE edge.
 * @returns "Puente" or "Camino".
 */
function connectionLabel(edge: EdgeGE): string {
  return edge.connection_type === "bridge" ? "Puente" : "Camino";
}

/**
 * Build the details of a GE vertex.
 *
 * @param vertex Vertex to describe.
 * @param edges Every GE edge.
 * @returns Fields (type, coordinates, degree) and incident connections.
 */
function describeVertex(vertex: VertexGE, edges: EdgeGE[]): VertexDetail {
  const style = POSITION_STYLES[vertex.position_type];
  const incident = incidentEdges(edges, vertex.id);
  return {
    id: vertex.id,
    typeLabel: style.label,
    tone: style.tone,
    fields: [
      { label: "Coordenadas", value: formatCoordinates(vertex.x, vertex.y) },
      { label: "Grado", value: formatNumber(incident.length) },
      {
        label: "Disponibles",
        value: formatNumber(incident.filter((edge) => edge.available).length),
      },
    ],
    connections: incident.map((edge) => ({
      edgeId: edge.id,
      neighborId: oppositeEnd(edge, vertex.id),
      summary: [connectionLabel(edge), describeTimes(edge), describeResistance(edge)]
        .filter(Boolean)
        .join(" · "),
      available: edge.available,
      highlighted: false,
    })),
  };
}

/**
 * Translate the GE API data into the generic graph view.
 *
 * @param data Vertices and edges of GE.
 * @returns View with nodes colored by position type, paths/bridges and
 *          labels with the foot and motorcycle times.
 */
export function buildElevatedView(data: ElevatedGraphData): GraphView {
  const byId = new Map(data.vertices.map((vertex) => [vertex.id, vertex]));

  return {
    kind: "ge",
    title: "Grafo elevado GE",
    description: "Posiciones del terreno unidas por caminos y puentes. Tiempos a pie y en moto.",
    nodes: data.vertices.map((vertex) => ({
      id: vertex.id,
      x: vertex.x,
      y: vertex.y,
      tone: POSITION_STYLES[vertex.position_type].tone,
      tooltip: `${vertex.id} · ${POSITION_STYLES[vertex.position_type].label}`,
    })),
    links: data.edges.map((edge) => ({
      id: edge.id,
      source: edge.v1,
      target: edge.v2,
      tone: edge.connection_type === "bridge" ? "bridge" : "path",
      label: [describeTimes(edge), describeResistance(edge)].filter(Boolean).join(" · "),
      available: edge.available,
      highlighted: false,
    })),
    legend: LEGEND,
    edgeRows: data.edges.map((edge) => ({
      id: edge.id,
      endpoints: `${edge.v1} — ${edge.v2}`,
      typeLabel: connectionLabel(edge),
      metrics: [describeTimes(edge), describeResistance(edge)].filter(Boolean).join(" · "),
      statusLabel: describeStatus(edge),
      available: edge.available,
      highlighted: false,
    })),
    vertexIds: data.vertices.map((vertex) => vertex.id),
    describeVertex: (vertexId) => {
      const vertex = byId.get(vertexId);
      return vertex ? describeVertex(vertex, data.edges) : null;
    },
  };
}
