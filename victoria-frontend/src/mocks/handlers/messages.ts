import { http, HttpResponse } from "msw"

export const handlers = [
    http.get('/api/messages/:id', ({params: { id }}) => {
        switch (id) {
            case '1':
                return HttpResponse.json(
                    {
                        id: 1,
                        type: 'markdown',
                        content: "This is **markdown**!!"
                    }
                )
            case '2':
                return HttpResponse.json(
                    {
                        id: 2,
                        type: 'image'
                    }
                )
            case '3':
                return HttpResponse.json(
                    {
                        id: 2,
                        type: 'choice-prompt'
                    }
                )
            case '4':
                return HttpResponse.json(
                    {
                        id: 2,
                        type: 'action-confirmation'
                    }
                )
        }
    }),
]