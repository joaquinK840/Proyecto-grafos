import { useEffect, useState } from "react";
import { graphApi } from "../services/graphApi";
import type { ElevatedGraphData, MazeGraphData } from "../types/graph";
import type { ScenarioSummary } from "../types/scenario";

/** Both graphs of the loaded scenario. */
export interface ScenarioGraphs {
  ge: ElevatedGraphData;
  gm: MazeGraphData;
}

/**
 * Load GE and GM every time the scenario summary changes.
 *
 * Both graphs are fetched together so switching between them in the UI is
 * instant. A new summary object (after loading or refreshing) triggers a
 * new fetch; answers from an outdated request are ignored.
 *
 * @param summary Current scenario summary, or `null` when none is loaded.
 * @returns `graphs` (null without scenario), `isLoading` and `error`.
 */
export function useScenarioGraphs(summary: ScenarioSummary | null) {
  const [graphs, setGraphs] = useState<ScenarioGraphs | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!summary) {
      setGraphs(null);
      return;
    }

    let isCurrent = true;
    setIsLoading(true);
    setError(null);

    Promise.all([graphApi.getElevatedGraph(), graphApi.getMazeGraph()])
      .then(([ge, gm]) => {
        if (isCurrent) setGraphs({ ge, gm });
      })
      .catch((cause: unknown) => {
        if (isCurrent) {
          setError(cause instanceof Error ? cause.message : "No se pudieron cargar los grafos.");
        }
      })
      .finally(() => {
        if (isCurrent) setIsLoading(false);
      });

    return () => {
      isCurrent = false;
    };
  }, [summary]);

  return { graphs, isLoading, error };
}
