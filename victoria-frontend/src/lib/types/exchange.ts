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

export const InitialExchanges = z.object({
	type: z.literal("initial"),
	exchanges: z.array(Exchange)
});
export type InitialExchanges = z.infer<typeof InitialExchanges>;

export const NewExchange = z.object({
	type: z.literal("new"),
	exchange: Exchange
});
export type NewExchange = z.infer<typeof NewExchange>;

export const ExchangeListingEvent = z.discriminatedUnion("type", [InitialExchanges, NewExchange]);
export type ExchangeListingEvent = z.infer<typeof Exchange>;
