import { http, HttpResponse } from "msw"

export const handlers = [
    http.get('/api/action-repos', () => {
        return HttpResponse.json([
            {
                id: 1,
                name: "Home assistant tools",
                url: "http://golem/PistaMista/HA-tools.git"
            }
        ])
    }),
    http.post('/api/action-repos', () => {
        return HttpResponse.json(
            {
                id: 2
            }
        )
    }),
    
    http.get('/api/action-repos/:id', ({ params: { id }}) => {
        switch (id) {
            case '1':
                return HttpResponse.json([
                    {
                        id: 1,
                        name: "Home assistant tools",
                        url: "http://golem/PistaMista/HA-tools.git"
                    }
                ])
        }
    }),
    http.put('/api/action-repos/:id', () => {
        return HttpResponse.json(true)
    }),
    http.delete('/api/action-repos/:id', () => {
        return HttpResponse.json(true)
    }),
]