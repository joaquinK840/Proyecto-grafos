import type { ScenarioSummary } from "../types/scenario";
import { ApiError, request } from "./httpClient";

/** HTTP calls for scenarios. */
export const scenarioApi = {
  /**
   * Send a scenario JSON to be validated, built and stored.
   *
   * @param payload Parsed content of the scenario file.
   * @returns Summary of the loaded scenario.
   */
  load: (payload: unknown) =>
    request<ScenarioSummary>("/scenarios/load", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  /**
   * Get the summary of the scenario currently loaded in the backend.
   *
   * @returns The summary, or `null` when no scenario has been loaded (HTTP 409).
   */
  getCurrent: async (): Promise<ScenarioSummary | null> => {
    try {
      return await request<ScenarioSummary>("/scenarios/current");
    } catch (cause) {
      if (cause instanceof ApiError && cause.status === 409) return null;
      throw cause;
    }
  },
};
