import { http, HttpResponse } from "msw"
import type { Model } from "$lib/types/model"

export const handlers = [
    http.get('/api/models', () => {
        return HttpResponse.json<Array<Model>>([
            {
                id: 1,
                connectionId: 2,
                name: 'gemma3:12b',
                enabled: true
            }
        ])
    }),
    http.post('/api/models/:id/enable', () => {
        return HttpResponse.json<Boolean>(true)
    }),
    http.post('/api/models/:id/disable', () => {
        return HttpResponse.json<Boolean>(false)
    }),
]