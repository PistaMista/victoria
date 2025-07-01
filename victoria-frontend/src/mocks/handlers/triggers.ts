import { http, HttpResponse } from "msw"
import { TriggerListItem, Trigger } from "$lib/types/trigger"

export const handlers = [
    http.get('/api/triggers', () => {
        return HttpResponse.json<Array<TriggerListItem>>([
            {
                id: 1,
                name: 'Generate recipes',
                type: 'timer',
            },
            {
                id: 2,
                name: 'Check news',
                type: 'poll',
            },
            {
                id: 3,
                name: 'General chat messages',
                type: 'chat',
            },
            {
                id: 4,
                name: 'Discord message received',
                type: 'webhook',
            }
        ])
    }),
    http.post('/api/triggers', () => {
        return HttpResponse.json<TriggerListItem>({
            id: 5,
            name: 'A new trigger',
            type: 'timer'
        })
    }),

    http.get('/api/triggers/:id', ({ params: { id }}) => {
        switch (id) {
            case '1':
                return HttpResponse.json<Trigger>({
                    id: 1,
                    name: 'Generate recipes',
                    settings: {
                        type: 'timer',
                        interval: "2d"
                    },
                    parser: "identity",
                    template: "Based on the feed from the fridge camera, generate recipes for the week"
                })
            case '2':
                return HttpResponse.json<Trigger>({
                    id: 2,
                    name: 'Retrieve news',
                    settings: {
                        type: 'poll',
                        interval: "1h",
                        url: "https://bbc.co.uk/rss"
                    },
                    parser: "identity",
                    template: "Based on the following news from BBC, notify the user of anything interesting: ${content}"                    
                })
            case '3':
                return HttpResponse.json<Trigger>({
                    id: 3,
                    name: 'General chat',
                    settings: {
                        type: 'chat',
                        receiver: "general"
                    },
                    parser: "identity",
                    template: "A new chat message has arrived from the user: ${content}"                    
                })
            case '4':
                return HttpResponse.json<Trigger>({
                    id: 4,
                    name: 'Discord chat message received',
                    settings: {
                        type: 'webhook',
                        url: "/hook"
                    },
                    parser: "identity",
                    template: "A new message has been sent in the #tech-talk discord channel: ${content}"                    
                })
        }
    }),
    http.put('/api/triggers/:id', () => {
        return HttpResponse.json<Boolean>(true)
    }),
    http.delete('/api/triggers/:id', () => {
        return HttpResponse.json<Boolean>(true)
    }),
]