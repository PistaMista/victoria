import { http, HttpResponse } from "msw"

export const handlers = [
    http.get('/api/triggers', () => {}),
    http.post('/api/triggers', () => {}),

    http.get('/api/triggers/:id', () => {}),
    http.put('/api/triggers/:id', () => {}),
    http.delete('/api/triggers/:id', () => {}),
]