import { writable, get } from 'svelte/store';
import type { Writable } from 'svelte/store';
import { Message as MessageSchema, SubscriptionState } from "$lib/types/websocket";
import type { Subscription, Message, PongHeartbeatMessage, HandlerSubscription, EventHandler } from "$lib/types/websocket";

export type SocketStatus = {
	connected: boolean,
	reconnectAttemptIdx: number
};

export let socketStatus: Writable<SocketStatus> = writable({
	connected: false,
	reconnectAttemptIdx: 0
});

let socket: WebSocket | null = null;
let handlerIdCounter: number = 0;

let subscriptions: Map<number, Writable<HandlerSubscription>> = new Map();

/**
 * Connects to the websocket endpoint.
 */
export function connectWithRetry(): void {
	if (socket !== null) return;

	const url = new URL('/websocket', window.location.href);
	url.protocol = url.protocol === 'https:' ? 'wss:' : 'ws:';

	socket = new WebSocket(url);

	socket.onmessage = (ev: MessageEvent) => {
		const json = JSON.parse(ev.data.toString());
		const msg = MessageSchema.parse(json);
		receiveMessage(msg);
	};

	socket.onclose = () => {
		socketStatus.update((val) => ({ ...val, connected: false, reconnectAttemptIdx: val.reconnectAttemptIdx + 1 }));

		updateSubscriptionStateOnConnectionLoss();
		socket = null;
		setTimeout(connectWithRetry, 1000);
	};

	socket.onopen = () => {
		socketStatus.update((val) => ({ ...val, connected: true, reconnectAttemptIdx: 0 }));
		sendPendingMessages();
	};
}

/**
 * Disconnects the websocket and all event subscriptions.
 */
export function disconnect(): void {
	if (socket === null) return;
	socketStatus.update((val) => ({ ...val, connected: false }));
	socket.onclose = null;
	socket.close();
	socket = null;

	for (const sub of subscriptions.values()) {
		sub.update((val) => ({ ...val, state: SubscriptionState.Cancelled, requestSent: true }));
	}
	subscriptions.clear();
}

/**
 * Subscribes to a particular event.
 *
 * @param subscription Details about the requested subscription.
 * @param handler The function to handle incoming messages.
 *
 * @returns A handle that can be used to unsubscribe from the event.
 */
export function subscribeEvent(subscription: Subscription, handler: EventHandler): Writable<HandlerSubscription> {
	const newHandlerId = handlerIdCounter++;
	const pendingSubscription: Writable<HandlerSubscription> = writable({
		subscriptionInfo: subscription,
		state: SubscriptionState.Subscribing,
		cancelReason: "",
		requestSent: false,
		unsubscribeHandle: () => { unsubscribeEvent(newHandlerId); },
		handler: handler,
	});
	subscriptions.set(newHandlerId, pendingSubscription);

	sendPendingMessages();

	return pendingSubscription;
}

/**
 * Unsubscribes from a particular event.
 *
 * @param handlerId The handler ID to unsubscribe.
 */
function unsubscribeEvent(handlerId: number): void {
	const sub = subscriptions.get(handlerId);

	if (sub) {
		sub.update((val) => ({ ...val, state: SubscriptionState.Cancelling, requestSent: false }));
	}

	sendPendingMessages();
}

/**
 * Receives and processes a given message.
 *
 * @param msg The message to process.
 */
function receiveMessage(msg: Message): void {
	switch (msg.type) {
		case "subscribeResponse":
			let handlerId = msg.handlerId;

			const subscription = subscriptions.get(handlerId);

			if (subscription) {
				if (msg.success) {
					subscription.update((val) => ({ ...val, state: SubscriptionState.Subscribed }));
				} else {
					subscription.update((val) => ({ ...val, state: SubscriptionState.Cancelled, cancelReason: msg.reason }));
				}
			}
			break;

		case "subscriptionCancelled":
			let sub = subscriptions.get(msg.handlerId);

			if (sub !== undefined) {
				sub.update((val) => ({ ...val, state: SubscriptionState.Cancelled }));
				subscriptions.delete(msg.handlerId);
			}

			break;

		case "ping":
			if (socket !== null && socket.readyState == WebSocket.OPEN) {
				const reply: PongHeartbeatMessage = {
					type: "pong",
				};
				const replyJson = JSON.stringify(reply);
				socket.send(replyJson);
			}
			break;

		case "eventMessage":
			for (const handlerId of msg.handlerIds) {
				const subs = subscriptions.get(handlerId);
				if (subs) {
					const sub = get(subs);
					if (sub.state === SubscriptionState.Subscribed) {
						sub.handler(msg.content);
					}
				}
			}
			break;
	}
}

/**
 * Sends requests for Subscribing and Cancelling subscriptions whose requests have not been sent.
 */
function sendPendingMessages(): void {
	for (const [id, store] of subscriptions) {
		store.update((val) => {
			if (val.requestSent || socket === null || socket.readyState != WebSocket.OPEN) return val;

			let msg: Message | null = null;
			switch (val.state) {
				case SubscriptionState.Subscribing:
					msg = {
						type: "subscribeRequest",
						handlerId: id,
						subscription: val.subscriptionInfo
					};
					break;
				case SubscriptionState.Cancelling:
					msg = {
						type: "unsubscribeRequest",
						handlerId: id
					};
					break;
			}

			if (msg) {
				const msgJson = JSON.stringify(msg);
				try {
					socket.send(msgJson);
					return { ...val, requestSent: true };
				} catch (e) {
					console.log((e as Error).message);
				}
			}

			return val;
		});
	}
}

/**
 * Puts all Subscribed subscriptions in a Subscribing state (to retry subscription later).
 */
function updateSubscriptionStateOnConnectionLoss(): void {
	for (const store of subscriptions.values()) {
		store.update((val) => {
			switch (val.state) {
				case SubscriptionState.Subscribing:
				case SubscriptionState.Subscribed:
					return { ...val, state: SubscriptionState.Subscribing, requestSent: false }
				case SubscriptionState.Cancelling:
				case SubscriptionState.Cancelled:
					return { ...val, state: SubscriptionState.Cancelled, requestSent: true };
			}
		});
	}
}
