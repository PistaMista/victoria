import { z } from "zod";

export const Action = z.object({
  id: z.number(),
  repoId: z.number().nullable(),
  name: z.string(),
  displayName: z.string(),
});

export type Action = z.infer<typeof Action>;
