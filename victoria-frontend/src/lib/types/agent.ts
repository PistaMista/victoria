import { z } from "zod";

export const AgentStatus = z.enum(["IDLE", "BUSY"]);
export type AgentStatus = z.infer<typeof AgentStatus>;

export const ModelParameters = z.object({
	temperature: z.number(),
	top_k: z.number(),
});
export type ModelParameters = z.infer<typeof ModelParameters>;

export const Agent = z.object({
	id: z.number(),
	name: z.string(),
	thumbnailDataURI: z.string().nullable(),
	status: AgentStatus,
	baseModelId: z.number().nullable(),
	systemPrompt: z.string(),
	modelParameters: ModelParameters,
	enabledTriggers: z.array(z.number()),
	enabledActions: z.array(z.number()),
});
export type Agent = z.infer<typeof Agent>;

export const AgentListItem = z.object({
	id: z.number(),
	name: z.string(),
	status: AgentStatus,
});
export type AgentListItem = z.infer<typeof AgentListItem>;
