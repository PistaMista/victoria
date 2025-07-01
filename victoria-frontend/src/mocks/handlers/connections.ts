import { http, HttpResponse } from "msw"

export const handlers = [
    http.get('/api/connections', () => {}),
    http.post('/api/connections', () => {}),

    http.get('/api/connections/:id', () => {}),
    http.put('/api/connections/:id', () => {}),
    http.delete('/api/connections/:id', () => {}),
]