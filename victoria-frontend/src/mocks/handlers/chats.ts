import { http, HttpResponse } from "msw"
import { ChatOptions, type Chat, type SentMessageInfo } from "$lib/types/chat"

export const handlers = [
    http.get('/api/chats', ({request}) => {
        const url = new URL(request.url);
        const sortBy = url.searchParams.get('sortBy');
        const receiver = url.searchParams.get('receiver');
        
        const chats = {
            admin: {
                id: 1,
                rootExchangeId: 1,
                title: "System admin",
                summary: "Chat about system administration."
            },
            learning: {
                id: 2,
                rootExchangeId: 2,
                title: "Language learning",
                summary: "Discussing ways to learn languages effectively."
            }
        }
        
        switch (receiver) {
            case 'general':
                return HttpResponse.json<Array<Chat>>(
                    [
                        chats.admin
                    ]
                )

            case 'research':
                return HttpResponse.json<Array<Chat>>(
                    [
                        chats.learning
                    ]
                )
        }
        
        switch (sortBy) {
            case 'importance':
                return HttpResponse.json<Array<Chat>>(
                    [
                        chats.learning,
                        chats.admin
                    ]
                )
            case 'length':
            case 'recent':
                return HttpResponse.json<Array<Chat>>(
                    [
                        chats.admin,
                        chats.learning
                    ]
                )
        }
    }),
    http.post('/api/chats', () => {
        return HttpResponse.json<Chat>(
            {
                id: 3,
                rootExchangeId: null,
                title: "New chat",
                summary: "A chat about nothing in particular (yet)."                
            }
        )
    }),
    http.delete('/api/chats/:id', () => {
        return HttpResponse.json<Boolean>(true)
    }),

    // This returns the ID of the created exchange
    http.post('/api/chats/:id/send-message', () => {
        return HttpResponse.json<SentMessageInfo>(
            {
                exchangeId: 3
            }
        )
    }),

    http.get('/api/chats/:id/options', () => {
        return HttpResponse.json<ChatOptions>(
            {
                receiver: 'general',
                enabledActionIds: [1, 2, 3, 5]
            }
        )
    }),
    http.put('/api/chats/:id/options', () => {
        return HttpResponse.json<ChatOptions>(
            {
                receiver: 'research',
                enabledActionIds: [1, 4]
            }
        )
    }),
]