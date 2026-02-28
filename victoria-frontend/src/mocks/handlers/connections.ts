import { http, HttpResponse } from "msw";
import { Connection, ConnectionListItem } from "$lib/types/connection";
import { spy } from "../spy";

export const listConnectionsHandler = await spy(() => {
  return HttpResponse.json<Array<ConnectionListItem>>([
    {
      id: 1,
      name: "Homelab",
    },
  ]);
});

export const createConnectionHandler = await spy(() => {
  return HttpResponse.json<ConnectionListItem>({
    id: 1,
    name: "Homelab",
  });
});

export const getConnectionHandler = await spy(({ params: { id } }) => {
  return HttpResponse.json<Connection>({
    id: Number(id),
    name: "Homelab",
    url: "http://golem:11434",
  });
});

export const updateConnectionHandler = await spy(() => {
  return HttpResponse.json<Boolean>(true);
});

export const deleteConnectionHandler = await spy(() => {
  return HttpResponse.json<Boolean>(true);
});

export const handlers = [
  http.get("/api/connections", listConnectionsHandler),
  http.post("/api/connections", createConnectionHandler),

  http.get("/api/connections/:id", getConnectionHandler),
  http.put("/api/connections/:id", updateConnectionHandler),
  http.delete("/api/connections/:id", deleteConnectionHandler),
];
