import { z } from "zod";

export const Event = z.object({
	triggerId: z.number(),
	content: z.string(),
});
export type Event = z.infer<typeof Event>;
