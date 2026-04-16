import { ws } from "msw";
import { spy } from "../spy";
import { EventMessage, SubscribeResponseMessage } from "$lib/types/websocket";
import { socketSendExchanges } from "./chats";
import { socketSendMessages } from "./exchanges";
import { socketSendMonologueStatus, socketSendMonologueThoughts } from "./monologues";


const socket = ws.link("ws://localhost:3000/ws")

export const disconnectionHandler = await spy(() => { });

export const connectionHandler = await spy(async ({ client }) => {
	client.addEventListener('message', async (event: any) => {
		const data = JSON.parse(event.data);

		switch (data.type) {
			case "subscribeRequest":
				switch (data.subscription.type) {
					case 'test':
						if (data.subscription.declineRequest) {
							client.send(JSON.stringify({
								type: "subscribeResponse",
								handlerId: data.handlerId,
								success: false,
								reason: "TEST REFUSE"
							} as SubscribeResponseMessage));
						} else {
							client.send(JSON.stringify({
								type: "subscribeResponse",
								handlerId: data.handlerId,
								success: true,
								reason: "succeeded"
							} as SubscribeResponseMessage));

							client.send(JSON.stringify({
								type: "eventMessage",
								handlerIds: [6000, data.handlerId],
								content: data.subscription.replyWith
							} as EventMessage));
						}
						break;
					case 'chat_exchanges':
						client.send(JSON.stringify({
							type: "subscribeResponse",
							handlerId: data.handlerId,
							success: true,
							reason: "succeeded"
						} as SubscribeResponseMessage));

						await socketSendExchanges(client, data.handlerId);
						break;
					case 'exchange_agent_messages':
						client.send(JSON.stringify({
							type: "subscribeResponse",
							handlerId: data.handlerId,
							success: true,
							reason: "succeeded"
						} as SubscribeResponseMessage));

						await socketSendMessages(client, data.handlerId);
						break;
					case 'monologue_status':
						client.send(JSON.stringify({
							type: "subscribeResponse",
							handlerId: data.handlerId,
							success: true,
							reason: "succeeded"
						} as SubscribeResponseMessage));

						await socketSendMonologueStatus(client, data.handlerId, data.subscription.monologueId, data.subscription.sendInitial);
						break;

					case 'monologue_thoughts':
						client.send(JSON.stringify({
							type: "subscribeResponse",
							handlerId: data.handlerId,
							success: true,
							reason: "succeeded"
						} as SubscribeResponseMessage));

						await socketSendMonologueThoughts(client, data.handlerId);
						break;
				};
				break;
		};
	});

	client.addEventListener('close', disconnectionHandler);
});

export const handlers = [
	socket.addEventListener('connection', connectionHandler)
];

