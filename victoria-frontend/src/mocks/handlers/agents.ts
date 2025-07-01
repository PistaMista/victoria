import { http, HttpResponse } from "msw"
import type { Agent, AgentListItem } from "$lib/types/agent";
import { MonologueListItem } from "$lib/types/monologue";

export const handlers = [
    http.get('/api/agents', () => {
        return HttpResponse.json<Array<AgentListItem>>(
            [
                {
                    id: 1,
                    name: 'Cook',
                    status: 'BUSY'
                },
                {
                    id: 2,
                    name: 'Researcher',
                    status: 'IDLE'
                }
            ]
        )
    }),
    http.post('/api/agents', async ({ request }) => {
        const body = await request.json() as {
            name: string
        };

        return HttpResponse.json<AgentListItem>(
            {
                id: 3,
                name: body.name,
                status: 'IDLE'
            }
        )
    }),
    
    http.get('/api/agents/:id', ({params: { id }}) => {
        return HttpResponse.json<Agent>({
            id: Number(id),
            name: "Cook",
            status: 'IDLE',
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
        return HttpResponse.json<Boolean>(true)
    }),
    http.delete('/api/agents/:id', () => {
        return HttpResponse.json<Boolean>(true)
    }),

    http.get('/api/agents/:id/monologues', () => {
        return HttpResponse.json<Array<MonologueListItem>>(
            [
                {
                    id: 1,
                    title: "Research thesis ideas",
                    summary: "Searching web for sources",
                    status: "RUNNING"
                },
                {
                    id: 2,
                    title: "Respond to user message",
                    summary: "Done",
                    status: "SUCCESS"
                }
            ]
        )
    }),
]