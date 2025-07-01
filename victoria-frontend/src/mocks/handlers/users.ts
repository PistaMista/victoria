import { http, HttpResponse } from "msw"

export const handlers = [
    http.get('/api/users', () => {
        return HttpResponse.json([
            {
                id: 1,
                username: 'krystof',
                role: 'admin'
            }
        ])
    }),
    http.post('/api/users', () => {
        return HttpResponse.json({
            id: 2
        })
    }),
    
    http.get('/api/users/:id', () => {
        return HttpResponse.json({
            id: 1,
            username: 'krystof',
            role: 'admin',
            permittedActions: [1, 2, 3, 4],
            permittedTriggers: [1]
        })
    }),
    http.put('/api/users/:id', () => {
        return HttpResponse.json(true)
    }),
    http.delete('/api/users/:id', () => {
        return HttpResponse.json(true)
    }),
]