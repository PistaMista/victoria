import { http, HttpResponse, delay } from "msw"

export const handlers = [
    http.get('/api/exchanges/:id', ({ params: { id } }) => {
        switch (id) {
            case '1':
                return HttpResponse.json(
                    {
                        userMessageId: 1,
                        agentMessageIds: [1, 2, 3, 4],
                        monologueId: 1,
                        childExchangeIds: [2]
                    }
                )
            case '2':
                return HttpResponse.json(
                    {
                        userMessageId: 2,
                        agentMessageIds: [1],
                        monologueId: 2,
                        childExchangeIds: [3, 4]
                    }
                )
            case '3':
                return HttpResponse.json(
                    {
                        userMessageId: 3,
                        agentMessageIds: [1],
                        monologueId: 2,
                        childExchangeIds: []
                    }
                )
            case '4':
                return HttpResponse.json(
                    {
                        userMessageId: 2,
                        agentMessageIds: [1, 3, 4],
                        monologueId: 2,
                        childExchangeIds: []
                    }
                )
        }
    }),
    // This is an HTTP long poll for new messages
    http.get('/api/exchanges/:id/new-messages', async () => {
        await delay(3000);
        
        return HttpResponse.json(
            {
                newMessageId: 2
            }
        )
    }),
]