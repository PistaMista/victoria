import { z } from "zod";

export type UnsubscribeHandle = () => void;
export type EventHandler = (event: any) => void;

export enum SubscriptionState {
	Subscribing,
	Subscribed,
	Cancelling,
	Cancelled,
};

export type HandlerSubscription = {
	subscriptionInfo: Subscription,
	requestSent: boolean,
	state: SubscriptionState,
	cancelReason: string,
	handler: EventHandler,
	unsubscribeHandle: UnsubscribeHandle,
};

export const TestSubscription = z.object({
	type: z.literal("test"),
	replyWith: z.any(),
	declineRequest: z.boolean()
});
export type TestSubscription = z.infer<typeof TestSubscription>;

export const ChatExchangesSubscription = z.object({
	type: z.literal("chat_exchanges"),
	chatId: z.number(),
});
export type ChatExchangesSubscription = z.infer<typeof ChatExchangesSubscription>;

export const ExchangeMessagesSubscription = z.object({
	type: z.literal("exchange_messages"),
	exchangeId: z.number(),
});

export const MonologueStatusSubscription = z.object({
	type: z.literal("monologue_status"),
	monologueId: z.number(),
});
export type MonologueStatusSubscription = z.infer<typeof MonologueStatusSubscription>;

export const MonologueThoughtsSubscription = z.object({
	type: z.literal("monologue_thoughts"),
	monologueId: z.number(),
});
export type MonologueThoughtsSubscription = z.infer<typeof MonologueThoughtsSubscription>;

export const Subscription = z.discriminatedUnion("type", [
	TestSubscription,
	ChatExchangesSubscription,
	ExchangeMessagesSubscription,
	MonologueStatusSubscription,
	MonologueThoughtsSubscription
]);
export type Subscription = z.infer<typeof Subscription>;

export const SubscribeRequestMessage = z.object({
	type: z.literal("subscribeRequest"),
	handlerId: z.number(),
	subscription: Subscription,
});
export type SubscribeRequestMessage = z.infer<typeof SubscribeRequestMessage>;

export const SubscribeResponseMessage = z.object({
	type: z.literal("subscribeResponse"),
	handlerId: z.number(),
	success: z.boolean(),
	reason: z.string(),
});
export type SubscribeResponseMessage = z.infer<typeof SubscribeResponseMessage>;

export const UnsubscribeRequestMessage = z.object({
	type: z.literal("unsubscribeRequest"),
	handlerId: z.number(),
});
export type UnsubscribeRequestMessage = z.infer<typeof UnsubscribeRequestMessage>;

export const UnsubscribeResponseMessage = z.object({
	type: z.literal("unsubscribeResponse"),
	handlerId: z.number(),
	success: z.boolean(),
	reason: z.string(),
});
export type UnsubscribeResponseMessage = z.infer<typeof UnsubscribeResponseMessage>;

export const SubscriptionCancelledMessage = z.object({
	type: z.literal("subscriptionCancelled"),
	handlerId: z.number(),
});
export type SubscriptionCancelledMessage = z.infer<typeof SubscriptionCancelledMessage>;

export const EventMessage = z.object({
	type: z.literal("eventMessage"),
	handlerIds: z.array(z.number()),
	content: z.any()
});
export type EventMessage = z.infer<typeof EventMessage>;

export const PingHeartbeatMessage = z.object({
	type: z.literal("ping"),
});
export type PingHeartbeatMessage = z.infer<typeof PingHeartbeatMessage>;

export const PongHeartbeatMessage = z.object({
	type: z.literal("pong"),
});
export type PongHeartbeatMessage = z.infer<typeof PongHeartbeatMessage>;

export const Message = z.discriminatedUnion("type", [
	SubscribeRequestMessage,
	SubscribeResponseMessage,
	UnsubscribeRequestMessage,
	UnsubscribeResponseMessage,
	SubscriptionCancelledMessage,
	PingHeartbeatMessage,
	PongHeartbeatMessage,
	EventMessage
]);
export type Message = z.infer<typeof Message>;
