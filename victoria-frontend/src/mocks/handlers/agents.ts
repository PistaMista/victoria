import { http, HttpResponse } from "msw"
import type { Agent, AgentListItem } from "$lib/types/agent";
import { MonologueListItem } from "$lib/types/monologue";
import { spy } from "../spy";

export const listAgentsHandler = await spy(
    () => {
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
    }   
)

export const createAgentHandler = await spy(
 async ({ request }) => {
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
    }   
)

export const getAgentHandler = await spy(
    ({params: { id }}) => {
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
    }   
)

export const updateAgentHandler = await spy(
    () => {
        return HttpResponse.json<Boolean>(true)
    }   
)

export const deleteAgentHandler = await spy(
    () => {
        return HttpResponse.json<Boolean>(true)
    }   
)

export const getAgentMonologuesHandler = await spy(
    () => {
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
    }   
)

export const handlers = [
    http.get('/api/agents', listAgentsHandler),
    http.post('/api/agents', createAgentHandler),
    
    http.get('/api/agents/:id', getAgentHandler),
    http.put('/api/agents/:id', updateAgentHandler),
    http.delete('/api/agents/:id', deleteAgentHandler),

    http.get('/api/agents/:id/monologues', getAgentMonologuesHandler),
]