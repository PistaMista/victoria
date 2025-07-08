import { http, HttpResponse } from "msw"
import { ChatOptions, type Chat, type SentMessageInfo } from "$lib/types/chat"
import { spy } from "../spy";

export const listChatsHandler = await spy(({request}) => 
    {
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
    }
);

export const chatCreateHandler = await spy(
    () => {
        return HttpResponse.json<Chat>(
            {
                id: 3,
                rootExchangeId: null,
                title: "New chat",
                summary: "A chat about nothing in particular (yet)."                
            }
        )
    }
);

export const chatDeleteHandler = await spy(
    () => {
        return HttpResponse.json<Boolean>(true)
    }   
)

export const sendMessageHandler = await spy(
    () => {
        return HttpResponse.json<SentMessageInfo>(
            {
                exchangeId: 3
            }
        )
    }   
)

export const getChatOptionsHandler = await spy(
    () => {
        return HttpResponse.json<ChatOptions>(
            {
                receiver: 'general',
                enabledActionIds: [1, 3]
            }
        )
    }   
)

export const setChatOptionsHandler = await spy(
    () => {
        return HttpResponse.json<ChatOptions>(
            {
                receiver: 'research',
                enabledActionIds: [1, 4]
            }
        )
    }   
)

export const listChatReceiversHandler = await spy(
    () => {
        return HttpResponse.json<string[]>(
            ['general', 'research']
        )
    }
)

export const handlers = [
    http.get('/api/chats', listChatsHandler),
    http.post('/api/chats', chatCreateHandler),
    http.delete('/api/chats/:id', chatDeleteHandler),

    // This returns the ID of the created exchange
    http.post('/api/chats/:id/send-message', sendMessageHandler),

    http.get('/api/chats/:id/options', getChatOptionsHandler),
    http.put('/api/chats/:id/options', setChatOptionsHandler),

    http.get('/api/chats/receivers', listChatReceiversHandler),
]