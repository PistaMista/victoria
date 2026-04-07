import { z } from "zod";

export const TriggerInvocation = z.object({
	type: z.literal("TriggerInvocation"),
	name: z.null(),
	parameters: z.object({
		eventId: z.number(),
	}),
});
export type TriggerInvocation = z.infer<typeof TriggerInvocation>;

export const ActionInvocation = z.object({
	type: z.literal("ActionInvocation"),
	name: z.string(),
	parameters: z.record(z.any()),
});
export type ActionInvocation = z.infer<typeof ActionInvocation>;

export const ThoughtInvocation = z.object({
	type: z.literal("ThoughtInvocation"),
	name: z.null(),
	parameters: z.object({
		thought: z.string(),
	}),
});
export type ThoughtInvocation = z.infer<typeof ThoughtInvocation>;

export const SuccessInvocation = z.object({
	type: z.literal("SuccessInvocation"),
	name: z.null(),
	parameters: z.object({}),
});
export type SuccessInvocation = z.infer<typeof SuccessInvocation>;

export const FailureInvocation = z.object({
	type: z.literal("FailureInvocation"),
	name: z.null(),
	parameters: z.object({}),
});
export type FailureInvocation = z.infer<typeof SuccessInvocation>;

export const Thought = z.object({
	id: z.number(),
	startTimestamp: z.number().gte(0),
	invocation: z.discriminatedUnion("type", [
		TriggerInvocation,
		ActionInvocation,
		ThoughtInvocation,
		SuccessInvocation,
		FailureInvocation,
	]),
	result: z.string(),
});
export type Thought = z.infer<typeof Thought>;

export const InitialThoughts = z.object({
	type: z.literal("initial"),
	thoughts: z.array(Thought),
});
export type InitialThoughts = z.infer<typeof InitialThoughts>;

export const NewThought = z.object({
	type: z.literal("new"),
	thought: Thought
});
export type NewThought = z.infer<typeof NewThought>;

export const ThoughtListingEvent = z.discriminatedUnion("type", [InitialThoughts, NewThought]);
export type ThoughtListingEvent = z.infer<typeof ThoughtListingEvent>;

