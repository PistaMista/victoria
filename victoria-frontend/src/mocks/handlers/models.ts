import { http, HttpResponse } from "msw"
import type { Model } from "$lib/types/model"
import { spy } from "../spy"

export const listModelsHandler = await spy(
    () => {
        return HttpResponse.json<Array<Model>>([
            {
                id: 1,
                connectionId: 2,
                name: 'gemma3:12b',
                enabled: true
            }
        ])
    }   
)

export const enableModelHandler = await spy(
    () => {
        return HttpResponse.json<Boolean>(true)
    }   
)

export const disableModelHandler = await spy(
    () => {
        return HttpResponse.json<Boolean>(false)
    }   
)

export const handlers = [
    http.get('/api/models', listModelsHandler),
    http.post('/api/models/:id/enable', enableModelHandler),
    http.post('/api/models/:id/disable', disableModelHandler),
]