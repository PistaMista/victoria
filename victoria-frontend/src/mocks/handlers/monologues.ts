import { http, HttpResponse } from "msw"
import { Monologue, MonologueListItem } from "$lib/types/monologue"
import { Thought } from "$lib/types/thought"

export const handlers = [
    http.get('/api/monologues', () => {
        return HttpResponse.json<Array<MonologueListItem>>([
            {
                id: 1,
                status: "RUNNING",
                title: "Research thesis ideas",
                summary: "Searching the web for sources"
            },
            {
                id: 2,
                status: "SUCCESS",
                title: "Generate recipes for the week",
                summary: "Checking available ingredients"
            }
        ])
    }),
    http.get('/api/monologues/:id', ({params: { id }}) => {
        switch (id) {
            case '1':
                return HttpResponse.json<Monologue>({
                    id: 1,
                    agentId: 2,
                    status: "RUNNING",
                    title: "Research thesis ideas",
                    summary: "Searching the web for sources"
                })
            case '2':
                return HttpResponse.json<Monologue>({
                    id: 2,
                    agentId: 1,
                    status: "SUCCESS",
                    title: "Generate recipes for the week",
                    summary: "Checking available ingredients"
                })
                
        }
    }),
    
    http.get('/api/monologues/:id/thoughts', () => {
        return HttpResponse.json<Array<Thought>>([
            {
                id: 1,
                invocation: {
                    type: 'TriggerInvocation',
                    name: null,
                    parameters: {
                        eventId: 1
                    }
                },
                /// This is the content of the triggering event
                result: "An email has arrived..."
            },
            {
                id: 2,
                invocation: {
                    type: 'ThoughtInvocation',
                    name: null,
                    parameters: {
                        thought: "I should add the contained event to the calendar"
                    }
                },
                result: "I should add the contained event to the calendar"
            },
            {
                id: 3,
                invocation: {
                    type: 'ActionInvocation',
                    name: 'web_search',
                    parameters: {
                        query: "top 10 restaurants in Brno"
                    }
                },
                result: "[ { title: 'Some article title', summary: 'Some summary' } ]"
            },
            {
                id: 4,
                invocation: {
                    type: 'SuccessInvocation',
                    name: null,
                    parameters: { }
                },
                result: ""
            },
        ])
    }),
]