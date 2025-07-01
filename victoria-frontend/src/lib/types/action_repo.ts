import { z } from "zod"

export const ActionRepository = z.object({
    id: z.number(),
    name: z.string(),
    url: z.string()
})

export type ActionRepository = z.infer<typeof ActionRepository>;