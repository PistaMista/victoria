import { http, HttpResponse } from "msw"

export const handlers = [
    http.get('/api/thoughts/:id', () => {}),
]