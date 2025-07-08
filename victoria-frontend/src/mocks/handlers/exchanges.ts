import { http, HttpResponse, delay } from "msw"
import { Exchange } from "$lib/types/exchange"
import { Message } from "$lib/types/message"
import { spy } from "../spy"

export const getExchangeHandler = await spy(
    ({ params: { id } }) => {
        switch (id) {
            case '1':
                return HttpResponse.json<Exchange>(
                    {
                        userMessageId: 1,
                        agentMessageIds: [1, 2, 3, 4],
                        monologueIds: [1],
                        childExchangeIds: [2]
                    }
                )
            case '2':
                return HttpResponse.json<Exchange>(
                    {
                        userMessageId: 2,
                        agentMessageIds: [1],
                        monologueIds: [2, 1],
                        childExchangeIds: [3, 4]
                    }
                )
            case '3':
                return HttpResponse.json<Exchange>(
                    {
                        userMessageId: 3,
                        agentMessageIds: [1],
                        monologueIds: [2],
                        childExchangeIds: []
                    }
                )
            case '4':
                return HttpResponse.json<Exchange>(
                    {
                        userMessageId: 2,
                        agentMessageIds: [1, 3, 4],
                        monologueIds: [2],
                        childExchangeIds: []
                    }
                )
        }
    }   
)

export const newMessageHandler = await spy(
    async () => {
        await delay(3000);
        
        return HttpResponse.json<Message>(
            {
                id: 2,
                content: {
                    type: 'markdown',
                    markdownText: "weeee"
                }
            }
        )
    }   
)


export const handlers = [
    http.get('/api/exchanges/:id', getExchangeHandler),
    // This is an HTTP long poll for new messages
    http.get('/api/exchanges/:id/new-messages', newMessageHandler),
]