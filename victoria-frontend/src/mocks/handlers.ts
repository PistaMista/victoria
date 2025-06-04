import { http, HttpResponse } from "msw"

export const handlers = [
    http.post('/api/chat', () => {
        return HttpResponse.json({
            type: "assistant",
            content: "hello"
        })
    })
]