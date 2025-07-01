import { http, HttpResponse } from "msw"
import type { Event } from "$lib/types/event"

export const handlers = [
    http.get('/api/events/:id', () => {
        return HttpResponse.json<Event>({
            triggerId: 1,
            content: "An email has arrived: 'Join the 2025 game access conference...'"
        })
    }),
]