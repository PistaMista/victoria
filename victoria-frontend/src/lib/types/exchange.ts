import { z } from "zod";

export const Exchange = z.object({
    userMessageId: z.number(),
    agentMessageIds: z.array(z.number()),
    monologueId: z.number(),
    childExchangeIds: z.array(z.number()),
});
export type Exchange = z.infer<typeof Exchange>;