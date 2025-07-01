import { http, HttpResponse } from "msw"

export const handlers = [
    http.get('/api/monologues', () => {
        return HttpResponse.json([
            {
                id: 1,
                agentId: 2,
                status: "RUNNING",
                title: "Research thesis ideas",
                summary: "Searching the web for sources"
            },
            {
                id: 2,
                agentId: 1,
                status: "SUCCESS",
                title: "Generate recipes for the week",
                summary: "Checking available ingredients"
            }
        ])
    }),
    http.get('/api/monologues/:id', ({params: { id }}) => {
        switch (id) {
            case '1':
                return HttpResponse.json({
                    id: 1,
                    agentId: 2,
                    status: "RUNNING",
                    title: "Research thesis ideas",
                    summary: "Searching the web for sources"
                })
            case '2':
                return HttpResponse.json({
                    id: 2,
                    agentId: 1,
                    status: "SUCCESS",
                    title: "Generate recipes for the week",
                    summary: "Checking available ingredients"
                })
                
        }
    }),
    
    http.get('/api/monologues/:id/thoughts', () => {
        return HttpResponse.json([
            {
                id: 1
            },
            {
                id: 2
            },
            {
                id: 3
            },
            {
                id: 4
            },
        ])
    }),
]