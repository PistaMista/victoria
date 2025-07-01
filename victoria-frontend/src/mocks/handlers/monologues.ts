import { http, HttpResponse } from "msw"

export const handlers = [
    http.get('/api/monologues', () => {}),
    http.get('/api/monologues/:id', () => {}),
    
    http.get('/api/monologues/:id/thoughts', () => {}),
]