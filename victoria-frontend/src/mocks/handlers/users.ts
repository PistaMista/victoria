import { http, HttpResponse } from "msw"

export const handlers = [
    http.get('/api/users', () => {}),
    http.post('/api/users', () => {}),
    
    http.get('/api/users/:id', () => {}),
    http.put('/api/users/:id', () => {}),
    http.delete('/api/users/:id', () => {}),
]