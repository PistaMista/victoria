import { http, HttpResponse } from "msw"

export const handlers = [
    http.get('/api/connections', () => {
        return HttpResponse.json([
            {
                id: 1,
                name: "Homelab"           
            }
        ])
    }),
    http.post('/api/connections', () => {
        return HttpResponse.json([
            {
                id: 1,
                name: "Homelab"
            }
        ])
    }),

    http.get('/api/connections/:id', ({ params: { id } }) => {
        return HttpResponse.json({
            id: Number(id),
            name: "Homelab",
            url: "http://golem:11434"
        })
    }),
    http.put('/api/connections/:id', () => {
        return HttpResponse.json(true)
    }),
    http.delete('/api/connections/:id', () => {
        return HttpResponse.json(true)
    }),
]