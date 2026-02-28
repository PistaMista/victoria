import { http, HttpResponse } from "msw";
import type { Action } from "$lib/types/action";
import { spy } from "../spy";

export const getActionsHandler = await spy(() => {
  return HttpResponse.json<Array<Action>>([
    {
      id: 1,
      repoId: 1,
      name: "add_to_calendar",
      displayName: "Add to calendar",
    },
    {
      id: 2,
      repoId: null,
      name: "add_thought",
      displayName: "Think",
    },
    {
      id: 3,
      repoId: null,
      name: "start_monologue",
      displayName: "Start monologue",
    },
  ]);
});

export const handlers = [
  http.get("/api/actions", getActionsHandler), // This lists only permitted actions for the current user
  http.get("/api/actions/all", getActionsHandler), // This lists ALL existing actions
];
