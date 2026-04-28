import { z } from "zod";
import { ActionInvocation } from "./thought";

export const MarkdownContent = z.object({
	type: z.literal("markdown"),
	markdownText: z.string(),
});
export type MarkdownContent = z.infer<typeof MarkdownContent>;

export const ImageContent = z.object({
	type: z.literal("image"),
	imageDataURI: z.string(),
});
export type ImageContent = z.infer<typeof ImageContent>;

export const ChoicePromptContent = z.object({
	type: z.literal("choice_prompt"),
	queryId: z.number(),
	prompt: z.string(),
	choices: z.array(
		z.object({
			value: z.any(),
		}),
	),
});
export type ChoicePromptContent = z.infer<typeof ChoicePromptContent>;

export const ActionConfirmationContent = z.object({
	type: z.literal("action_confirmation"),
	invocationThought: ActionInvocation,
	queryId: z.number(),
});
export type ActionConfirmationContent = z.infer<
	typeof ActionConfirmationContent
>;

export const Message = z.object({
	id: z.number(),
	timestamp: z.number().gte(0),
	senderName: z.string(),
	content: z.discriminatedUnion("type", [
		MarkdownContent,
		ImageContent,
		ChoicePromptContent,
		ActionConfirmationContent,
	]),
});
export type Message = z.infer<typeof Message>;

export const InitialMessages = z.object({
	type: z.literal("initial"),
	messages: z.array(Message)
});
export type InitialMessages = z.infer<typeof InitialMessages>;

export const NewMessage = z.object({
	type: z.literal("new"),
	message: Message
});

export const MessageListingEvent = z.discriminatedUnion("type", [InitialMessages, NewMessage]);
export type MessageListingEvent = z.infer<typeof MessageListingEvent>;
