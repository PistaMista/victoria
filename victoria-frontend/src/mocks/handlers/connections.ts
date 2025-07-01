import { http, HttpResponse } from "msw"
import { Connection, ConnectionListItem } from "$lib/types/connection"

export const handlers = [
    http.get('/api/connections', () => {
        return HttpResponse.json<Array<ConnectionListItem>>([
            {
                id: 1,
                name: "Homelab"           
            }
        ])
    }),
    http.post('/api/connections', () => {
        return HttpResponse.json<Array<ConnectionListItem>>([
            {
                id: 1,
                name: "Homelab"
            }
        ])
    }),

    http.get('/api/connections/:id', ({ params: { id } }) => {
        return HttpResponse.json<Connection>({
            id: Number(id),
            name: "Homelab",
            url: "http://golem:11434"
        })
    }),
    http.put('/api/connections/:id', () => {
        return HttpResponse.json<Boolean>(true)
    }),
    http.delete('/api/connections/:id', () => {
        return HttpResponse.json<Boolean>(true)
    }),
]