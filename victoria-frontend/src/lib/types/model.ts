import { z } from "zod";

export const Model = z.object({
  id: z.number(),
  connectionId: z.number(),
  name: z.string(),
  enabled: z.boolean(),
});
export type Model = z.infer<typeof Model>;
