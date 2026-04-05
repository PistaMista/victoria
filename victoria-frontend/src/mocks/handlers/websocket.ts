import { ws } from "msw";
import { spy } from "../spy";

const socket = ws.link("ws://localhost:3000/websocket")

export const disconnectionHandler = await spy(() => { });

export const connectionHandler = await spy(({ client }) => {
	client.addEventListener('message', (event: any) => {
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
							}));
						} else {
							client.send(JSON.stringify({
								type: "subscribeResponse",
								handlerId: data.handlerId,
								success: true,
								reason: "succeeded"
							}));

							client.send(JSON.stringify({
								type: "eventMessage",
								handlerIds: [6000, data.handlerId],
								content: data.subscription.replyWith
							}));
						}
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

