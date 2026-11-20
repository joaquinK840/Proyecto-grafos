import type { ScenarioLoadResponse } from "../types/scenario";

async function loadJson(path: string, payload: unknown): Promise<ScenarioLoadResponse> {
  const response = await fetch(`/api/scenarios${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    let message = `Error ${response.status}: no se pudo cargar el escenario.`;
    try {
      const body: { detail?: string } = await response.json();
      if (body.detail) message = body.detail;
    } catch {
      // Se conserva el mensaje HTTP si la respuesta no contiene JSON.
    }
    throw new Error(message);
  }

  return response.json() as Promise<ScenarioLoadResponse>;
}

export const scenarioApi = {
  load: (payload: unknown) => loadJson("/load", payload),
};
