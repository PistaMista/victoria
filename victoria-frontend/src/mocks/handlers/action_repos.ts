import { http, HttpResponse } from "msw"

export const handlers = [
    http.get('/api/action-repos', () => {}),
    http.post('/api/action-repos', () => {}),
    
    http.get('/api/action-repos/:id', () => {}),
    http.put('/api/action-repos/:id', () => {}),
    http.delete('/api/action-repos/:id', () => {}),
]