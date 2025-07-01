import { http, HttpResponse } from "msw"

export const handlers = [
    http.get('/api/models', () => {
        return HttpResponse.json([
            {
                id: 1,
                connectionId: 2,
                name: 'gemma3:12b',
                enabled: true
            }
        ])
    }),
    http.post('/api/models/:id/enable', () => {
        return HttpResponse.json(true)
    }),
    http.post('/api/models/:id/disable', () => {
        return HttpResponse.json(false)
    }),
]