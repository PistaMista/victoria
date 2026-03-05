import { Deferred } from "$lib/types/deferred";
import { Message as MessageSchema } from "$lib/types/websocket";
import type { Subscription, Message, SubscribeRequestMessage, UnsubscribeRequestMessage } from "$lib/types/websocket";

type UnsubscribeHandle = () => Promise<void>;
type EventHandler = (event: any) => void;

type HandlerSubscription = {
	deferred: Deferred<UnsubscribeHandle>,
	handler: EventHandler
};

let socket: WebSocket | null = null;
let handlerIdCounter: number = 0;

let pendingSubscriptions: Map<number, HandlerSubscription> = new Map();
let subscribedHandlers: Map<number, EventHandler> = new Map();


export async function connectWithRetry(): Promise<void> {
	if (socket !== null) return;

	const url = new URL('/websocket', window.location.href);
	url.protocol = url.protocol === 'https:' ? 'wss:' : 'ws:';

	socket = new WebSocket(url);

	socket.onmessage = (ev: MessageEvent) => {
		const json = JSON.parse(ev.data);
		const msg = MessageSchema.parse(json);
		receiveMessage(msg);
	};

	socket.onclose = () => {
		cancelAllSubscriptions();
		socket = null;
		setTimeout(connectWithRetry, 1000);
	};
}

export async function disconnect(): Promise<void> {
	if (socket === null) return;
	socket.onclose = null;

	socket.close();
	cancelAllSubscriptions();

	socket = null;
}

export function subscribeEvent(subscription: Subscription, handler: EventHandler): Promise<UnsubscribeHandle> {
	if (socket === null) {
		throw Error("Websocket not connected");
	}

	const pendingSubscription: HandlerSubscription = {
		deferred: new Deferred<UnsubscribeHandle>(),
		handler: handler
	};
	const newHandlerId = handlerIdCounter++;
	pendingSubscriptions.set(newHandlerId, pendingSubscription);

	const msg: SubscribeRequestMessage = {
		type: "subscribeRequest",
		handlerId: newHandlerId,
		subscription: subscription
	};
	const msgJson = JSON.stringify(msg);
	socket.send(msgJson);

	return pendingSubscription.deferred.promise;
}

export function unsubscribeEvent(handlerId: number): void {
	if (socket === null) {
		throw Error("Websocket not connected");
	}

	pendingSubscriptions.delete(handlerId);
	subscribedHandlers.delete(handlerId);

	const msg: UnsubscribeRequestMessage = {
		type: "unsubscribeRequest",
		handlerId: handlerId,
	};
	const msgJson = JSON.stringify(msg);
	socket.send(msgJson);
}

function receiveMessage(msg: Message): void {
	switch (msg.type) {
		case "subscribeResponse":
			let handlerId = msg.handlerId;

			const subscription = pendingSubscriptions.get(handlerId);
			pendingSubscriptions.delete(handlerId);

			if (subscription) {
				if (!msg.success) {
					subscription.deferred.reject(msg.reason);
					return;
				}

				const unsubscribeHandle = async () => {
					unsubscribeEvent(handlerId);
				};

				subscribedHandlers.set(msg.handlerId, subscription.handler);
				subscription.deferred.resolve(unsubscribeHandle);
			}
			break;

		case "subscriptionCancelled":
			pendingSubscriptions.delete(msg.handlerId);
			subscribedHandlers.delete(msg.handlerId);
			break;

		case "eventMessage":
			for (const handlerId of msg.handlerIds) {
				const handler = subscribedHandlers.get(handlerId);
				if (handler) handler(msg.content);
			}
			break;
	}
}

function cancelAllSubscriptions(): void {
	for (const sub of pendingSubscriptions.values()) {
		sub.deferred.reject("Subscription cancelled (websocket was likely closed)");
	}

	pendingSubscriptions.clear();
	subscribedHandlers.clear();
}

