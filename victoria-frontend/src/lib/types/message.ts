import { z } from "zod";

export const Message = z.object({
    id: z.number(),
});
export type Message = z.infer<typeof Message>;