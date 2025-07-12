import { http, HttpResponse } from "msw"
import { spy } from "../spy"

export const answerQueryHandler = await spy(() => {
    return HttpResponse.json<boolean>(true);
})

export const handlers = [
    http.post('/queries/:id/answer', answerQueryHandler)
]