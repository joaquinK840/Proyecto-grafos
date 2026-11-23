import { useCallback, useEffect, useState } from "react";
import { scenarioApi } from "../services/scenarioApi";
import type { ScenarioSummary } from "../types/scenario";

/**
 * State of the scenario loaded in the backend.
 *
 * On mount it asks the backend for the current scenario, so reloading the
 * page keeps showing the scenario that is already loaded.
 *
 * @returns
 *  - `summary`: summary of the loaded scenario, or `null` if there is none.
 *  - `isLoading` / `error`: state of the last `refresh`.
 *  - `refresh()`: re-read the current scenario.
 *  - `load(payload)`: send a scenario JSON; throws if the backend rejects it.
 */
export function useScenario() {
  const [summary, setSummary] = useState<ScenarioSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      setSummary(await scenarioApi.getCurrent());
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "No se pudo consultar el escenario.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const load = useCallback(async (payload: unknown) => {
    const loaded = await scenarioApi.load(payload);
    setError(null);
    setSummary(loaded);
    return loaded;
  }, []);

  return { summary, isLoading, error, refresh, load };
}
