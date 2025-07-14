import { z } from "zod";

export const SentMessageInfo = z.object({
    exchangeId: z.number()
});
export type SentMessageInfo = z.infer<typeof SentMessageInfo>;

export const Chat = z.object({
    id: z.number(),
    title: z.string(),
    summary: z.string(),
});
export type Chat = z.infer<typeof Chat>;

export const ChatOptions = z.object({
    receiver: z.string(),
    enabledActionIds: z.array(z.number())
});
export type ChatOptions = z.infer<typeof ChatOptions>;