import { http, HttpResponse } from "msw"

export const handlers = [
    http.get('/api/agents', () => {
        return HttpResponse.json(
            [
                {
                    id: 1,
                    name: 'Cook'
                },
                {
                    id: 2,
                    name: 'Researcher'
                }
            ]
        )
    }),
    http.post('/api/agents', async ({ request }) => {
        const body = await request.json() as {
            name: string
        };

        return HttpResponse.json(
            {
                id: 3,
                name: body.name,
            }
        )
    }),
    
    http.get('/api/agents/:id', ({params: { id }}) => {
        return HttpResponse.json({
            id: Number(id),
            name: "Cook",
            baseModelId: 1,
            systemPrompt: "You're a Cook that generates recipes for the week...",
            modelParameters: {
                temperature: 0.5,
                top_k: 0.2
            },
            enabledTriggers: [1],
            enabledActions: [1, 2, 4]
        })
    }),
    http.put('/api/agents/:id', () => {
        return HttpResponse.json(true)
    }),
    http.delete('/api/agents/:id', () => {
        return HttpResponse.json(true)
    }),

    http.get('/api/agents/:id/monologues', () => {
        return HttpResponse.json(
            [
                {
                    id: 1,
                    title: "Research thesis ideas",
                    status: "RUNNING"
                },
                {
                    id: 2,
                    title: "Respond to user message",
                    status: "COMPLETED"
                }
            ]
        )
    }),
]