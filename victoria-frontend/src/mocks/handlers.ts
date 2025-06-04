import { http, HttpResponse } from "msw"

export const handlers = [
    http.get('/api/chat', () => {
        return HttpResponse.json({
            type: "assistant",
            content: "hello"
        })
    })
]