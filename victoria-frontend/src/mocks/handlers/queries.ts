import { http, HttpResponse } from "msw"
import { spy } from "../spy"

export const getAnsweredHandler = await spy(({params: { id }}) => {
    switch (id) {
        case '1':
            return HttpResponse.json<any>(true);
        case '2':
            return HttpResponse.json<any>(false);
        case '3':
            return HttpResponse.json<any>(null);
        case '4':
            return HttpResponse.json<any>([1, 2, 3]);
        default:
            return HttpResponse.json<any>(null);
    }
})

export const answerQueryHandler = await spy(({params: { id }}) => {
    switch (id) {
        case '1':
            return HttpResponse.json<any>(true);
        case '2':
            return HttpResponse.json<any>(false);
        case '3':
            return HttpResponse.json<any>("lol");
        case '4':
            return HttpResponse.json<any>([1, 2, 3]);
        default:
            return HttpResponse.json<any>(null);
    }
})

export const handlers = [
    http.get('/queries/:id/answer', getAnsweredHandler),
    http.post('/queries/:id/answer', answerQueryHandler)
]