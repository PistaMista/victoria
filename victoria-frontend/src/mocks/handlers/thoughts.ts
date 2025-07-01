import { http, HttpResponse } from "msw"
import type { Thought } from "$lib/types/thought"

export const handlers = [
    http.get('/api/thoughts/:id', ({ params: { id }}) => {
        switch (id) {
            case '1':
                return HttpResponse.json<Thought>({
                    id: 1,
                    invocation: {
                        type: 'ThoughtInvocation',
                        name: null,
                        parameters: {
                            thought: "I should add the contained event to the calendar"
                        }
                    },
                    result: "I should add the contained event to the calendar"
                })
            case '2':
                return HttpResponse.json<Thought>({
                    id: 2,
                    invocation: {
                        type: 'FailureInvocation',
                        name: null,
                        parameters: { }
                    },
                    result: ""
                })
            case '3':
                return HttpResponse.json<Thought>({
                    id: 3,
                    invocation: {
                        type: 'SuccessInvocation',
                        name: null,
                        parameters: { }
                    },
                    result: ""
                })
            case '4':
                return HttpResponse.json<Thought>({
                    id: 4,
                    invocation: {
                        type: 'TriggerInvocation',
                        name: null,
                        parameters: {
                            eventId: 1
                        }
                    },
                    /// This is the content of the triggering event
                    result: "An email has arrived..."
                })
            case '5':
                return HttpResponse.json<Thought>({
                    id: 5,
                    invocation: {
                        type: 'ActionInvocation',
                        name: 'web_search',
                        parameters: {
                            query: "top 10 restaurants in Brno"
                        }
                    },
                    result: "[ { title: 'Some article title', summary: 'Some summary' } ]"
                })
        }
    }),
]