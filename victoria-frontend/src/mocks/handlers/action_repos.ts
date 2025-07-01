import { http, HttpResponse } from "msw"
import { ActionRepository } from "../../lib/types/action_repo"

export const handlers = [
    http.get('/api/action-repos', () => {
        return HttpResponse.json<Array<ActionRepository>>([
            {
                id: 1,
                name: "Home assistant tools",
                url: "http://golem/PistaMista/HA-tools.git"
            } as ActionRepository
        ])
    }),
    http.post('/api/action-repos', () => {
        return HttpResponse.json<ActionRepository>(
            {
                id: 2,
                name: "Something",
                url: "http://seznam.cz"
            }
        )
    }),
    
    http.get('/api/action-repos/:id', ({ params: { id }}) => {
        switch (id) {
            case '1':
                return HttpResponse.json<ActionRepository>(
                    {
                        id: 1,
                        name: "Home assistant tools",
                        url: "http://golem/PistaMista/HA-tools.git"
                    }
                )
        }
    }),
    http.put('/api/action-repos/:id', () => {
        return HttpResponse.json<Boolean>(true)
    }),
    http.delete('/api/action-repos/:id', () => {
        return HttpResponse.json<Boolean>(true)
    }),
]