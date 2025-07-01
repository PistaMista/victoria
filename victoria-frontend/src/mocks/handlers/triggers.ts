import { http, HttpResponse } from "msw"

export const handlers = [
    http.get('/api/triggers', () => {
        return HttpResponse.json([
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
        return HttpResponse.json({
            id: 5
        })
    }),

    http.get('/api/triggers/:id', ({ params: { id }}) => {
        switch (id) {
            case '1':
                return HttpResponse.json({
                    id: 1,
                    name: 'Generate recipes',
                    type: 'timer',
                    settings: {
                        interval: "2d"
                    },
                    parser: "identity",
                    template: "Based on the feed from the fridge camera, generate recipes for the week"
                })
            case '2':
                return HttpResponse.json({
                    id: 2,
                    name: 'Retrieve news',
                    type: 'poll',
                    settings: {
                        interval: "1h",
                        url: "https://bbc.co.uk/rss"
                    },
                    parser: "identity",
                    template: "Based on the following news from BBC, notify the user of anything interesting: ${content}"                    
                })
            case '3':
                return HttpResponse.json({
                    id: 3,
                    name: 'General chat',
                    type: 'poll',
                    settings: {
                        receiver: "general"
                    },
                    parser: "identity",
                    template: "A new chat message has arrived from the user: ${content}"                    
                })
            case '4':
                return HttpResponse.json({
                    id: 4,
                    name: 'Discord chat message received',
                    type: 'webhook',
                    settings: {
                        url: "/hook"
                    },
                    parser: "identity",
                    template: "A new message has been sent in the #tech-talk discord channel: ${content}"                    
                })
        }
    }),
    http.put('/api/triggers/:id', () => {
        return HttpResponse.json(true)
    }),
    http.delete('/api/triggers/:id', () => {
        return HttpResponse.json(true)
    }),
]