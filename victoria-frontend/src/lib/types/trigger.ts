import { z } from "zod";

export const TriggerType = z.enum(['timer', 'poll', 'chat', 'webhook']);
export type TriggerType = z.infer<typeof TriggerType>;

export const ParserType = z.enum(['identity']);
export type ParserType = z.infer<typeof ParserType>;

export const TriggerListItem = z.object({
    id: z.number(),
    name: z.string(),
    type: TriggerType,
});
export type TriggerListItem = z.infer<typeof TriggerListItem>;

export const TimerSettings = z.object({
    type: z.literal('timer'),
    interval: z.number().gt(0),
});
export type TimerSettings = z.infer<typeof TimerSettings>;

export const PollSettings = z.object({
    type: z.literal('poll'),
    interval: z.number().gt(0),
    url: z.string(),
});
export type PollSettings = z.infer<typeof PollSettings>;

export const ChatSettings = z.object({
    type: z.literal('chat'),
    receiver: z.string(),
});
export type ChatSettings = z.infer<typeof ChatSettings>;

export const WebhookSettings = z.object({
    type: z.literal('webhook'),
    url: z.string(),
});
export type WebhookSettings = z.infer<typeof WebhookSettings>;

export const Trigger = z.object({
    id: z.number(),
    name: z.string(),
    settings: z.discriminatedUnion('type', [TimerSettings, PollSettings, ChatSettings, WebhookSettings]),
    parser: ParserType,
    template: z.string(),
});
export type Trigger = z.infer<typeof Trigger>;