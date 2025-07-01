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
                        type: 'image',
                        content: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAVCAIAAADelck2AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAVZJREFUeNrUlM9OwkAQxme229Y/gMWkhCsGmngQEvUd4GZ4O9/AAzyB0fgGcFRClBOikpRqG2m73V2XJ9ga24PfefeXmW++GZQ3V5B8QeGyaxS2PrDv4tEiI0AolCFCCZSmEtEUBFe+lOA1p7DvADH0Tw0ClgEIkHDgIkdCqihjlTyp6w2jIJlO3wWX3a5bbxxCpqUjSim1FSxX2/F41modIeJiEQwGJ167VswY726fe2fHq+Xn7PHj8tx9uH/hXOYYo06KwphQ9Y5GT1HElCGWZYRh6jj2X9GGgaapxgfDoRdFaaViJUlWrZraj7m8fnvded3p1BFhPg/6/Vbb03uNm9jX0iklvh9PJiohotdrNJsVlnFdPhAvrk+DOMhji2Xv4p+mnGf6Rp09h6636406fnkU/mIZmWTUVEMiZuF7rrD/8/IRJlgZXIWl7oFbhtcqIT8CDAAeYYokfXCFwwAAAABJRU5ErkJggg=='
                    }
                )
            case '3':
                return HttpResponse.json(
                    {
                        id: 2,
                        type: 'choice-prompt',
                        content: {
                            queryId: 1,
                            choices: [
                                { value: 2 },
                                { value: "this is a value" },
                                { value: true }
                            ]
                        }
                    }
                )
            case '4':
                return HttpResponse.json(
                    {
                        id: 2,
                        type: 'action-confirmation',
                        content: {
                            queryId: 20
                        }
                    }
                )
        }
    }),
]