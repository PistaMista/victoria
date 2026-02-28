import { http, HttpResponse } from "msw";
import type { Event } from "$lib/types/event";
import { spy } from "../spy";

export const getEventHandler = await spy(() => {
  return HttpResponse.json<Event>({
    triggerId: 1,
    content: "An email has arrived: 'Join the 2025 game access conference...'",
  });
});

export const handlers = [http.get("/api/events/:id", getEventHandler)];
