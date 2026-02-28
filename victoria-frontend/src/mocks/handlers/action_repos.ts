import { http, HttpResponse } from "msw";
import { ActionRepository } from "../../lib/types/action_repo";
import { spy } from "../spy";

export const listActionReposHandler = await spy(() => {
  return HttpResponse.json<Array<ActionRepository>>([
    {
      id: 1,
      name: "Home assistant tools",
      url: "http://golem/PistaMista/HA-tools.git",
    } as ActionRepository,
  ]);
});

export const createActionRepoHandler = await spy(() => {
  return HttpResponse.json<ActionRepository>({
    id: 2,
    name: "Something",
    url: "http://seznam.cz",
  });
});

export const getActionRepoHandler = await spy(({ params: { id } }) => {
  switch (id) {
    case "1":
      return HttpResponse.json<ActionRepository>({
        id: 1,
        name: "Home assistant tools",
        url: "http://golem/PistaMista/HA-tools.git",
      });
  }
});

export const setActionRepoHandler = await spy(() => {
  return HttpResponse.json<Boolean>(true);
});

export const deleteActionRepoHandler = await spy(() => {
  return HttpResponse.json<Boolean>(true);
});

export const handlers = [
  http.get("/api/action-repos", listActionReposHandler),
  http.post("/api/action-repos", createActionRepoHandler),

  http.get("/api/action-repos/:id", getActionRepoHandler),
  http.put("/api/action-repos/:id", setActionRepoHandler),
  http.delete("/api/action-repos/:id", deleteActionRepoHandler),
];
