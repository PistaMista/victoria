import { http, HttpResponse } from "msw"

export const handlers = [
    http.get('/api/actions', () => {
        return HttpResponse.json([
            {
                id: 1,
                repoId: 1,
                name: "add_to_calendar",
                displayName: "Add to calendar"
            },
            {
                id: 2,
                repoId: null,
                name: "add_thought",
                displayName: "Think"
            },
            {
                id: 3,
                repoId: null,
                name: "start_monologue",
                displayName: "Start monologue"
            }
        ])
    }),
]