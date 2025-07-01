import { z } from "zod";

export const MonologueStatus = z.enum(['RUNNING', 'PENDING', 'SUCCESS', 'FAILURE']);
export type MonologueStatus = z.infer<typeof MonologueStatus>;

export const MonologueListItem = z.object({
    id: z.number(),
    title: z.string(),
    summary: z.string(),
    status: MonologueStatus,
});
export type MonologueListItem = z.infer<typeof MonologueListItem>;

export const Monologue = z.object({
    id: z.number(),
    agentId: z.number(),
    title: z.string(),
    summary: z.string(),
    status: MonologueStatus,
})
export type Monologue = z.infer<typeof Monologue>;