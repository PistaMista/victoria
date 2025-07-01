import { http, HttpResponse } from "msw"

export const handlers = [
    http.get('/api/agents', () => {}),
    http.post('/api/agents', () => {}),
    
    http.get('/api/agents/:id', () => {}),
    http.put('/api/agents/:id', () => {}),
    http.delete('/api/agents/:id', () => {}),

    http.get('/api/agents/:id/monologues', () => {}),
]