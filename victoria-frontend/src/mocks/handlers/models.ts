import { http, HttpResponse } from "msw"

export const handlers = [
    http.get('/api/models', () => {}),
    http.post('/api/models/:id/enable', () => {}),
    http.post('/api/models/:id/disable', () => {}),
]