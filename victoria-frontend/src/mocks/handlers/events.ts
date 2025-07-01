import { http, HttpResponse } from "msw"

export const handlers = [
    http.get('/api/events/:id', () => {
        return HttpResponse.json({
            triggerId: 1,
            content: "An email has arrived: 'Join the 2025 game access conference...'"
        })
    }),
]