import { z } from "zod";

export const ConnectionListItem = z.object({
	id: z.number(),
	name: z.string(),
});
export type ConnectionListItem = z.infer<typeof ConnectionListItem>;

export const Connection = z.object({
	id: z.number(),
	name: z.string(),
	url: z.string(),
});
export type Connection = z.infer<typeof Connection>;
