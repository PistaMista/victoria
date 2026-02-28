import { z } from "zod";
import { Message as MessageSchema } from "./message";

export const Exchange = z.object({
	id: z.number(),
	chatId: z.number(),
	timestamp: z.number(),
	userMessage: MessageSchema.nullable(),
	monologueIds: z.array(z.number()),
});
export type Exchange = z.infer<typeof Exchange>;
