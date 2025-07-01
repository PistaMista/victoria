import { http, HttpResponse } from "msw"
import { UserListItem, User } from "$lib/types/user"

export const handlers = [
    http.get('/api/users', () => {
        return HttpResponse.json<Array<UserListItem>>([
            {
                id: 1,
                username: 'krystof',
                role: 'admin'
            }
        ])
    }),
    http.post('/api/users', () => {
        return HttpResponse.json<UserListItem>({
            id: 2,
            username: 'john',
            role: 'user'
        })
    }),
    
    http.get('/api/users/:id', () => {
        return HttpResponse.json<User>({
            id: 1,
            username: 'krystof',
            role: 'admin',
            permittedActions: [1, 2, 3, 4],
            permittedTriggers: [1]
        })
    }),
    http.put('/api/users/:id', () => {
        return HttpResponse.json<Boolean>(true)
    }),
    http.delete('/api/users/:id', () => {
        return HttpResponse.json<Boolean>(true)
    }),
]