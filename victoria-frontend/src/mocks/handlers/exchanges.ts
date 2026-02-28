import { http, HttpResponse, delay } from "msw";
import { Exchange } from "$lib/types/exchange";
import { Message } from "$lib/types/message";
import { spy } from "../spy";

export const getMessagesHandler = await spy(async ({ request }) => {
	let url: URL = new URL(request.url);
	let after: number = Number(url.searchParams.get("after"));

	await delay(400);

	if (after < 5000) {
		return HttpResponse.json<Message[]>([
			{
				id: 2,
				timestamp: 5000,
				senderName: "Researcher",
				content: {
					type: "markdown",
					markdownText: "Agent message!",
				},
			},
		]);
	} else if (after < 7000) {
		return HttpResponse.json<Message[]>([
			{
				id: 3,
				timestamp: 6500,
				senderName: "Cook",
				content: {
					type: "choice_prompt",
					prompt: "Pick a thing",
					queryId: 1,
					choices: [{ value: "lol" }],
				},
			},
			{
				id: 4,
				timestamp: 7000,
				senderName: "John",
				content: {
					type: "action_confirmation",
					invocationThought: {
						type: "ActionInvocation",
						name: "add_to_calendar",
						parameters: {
							date: "20",
							delete: true,
						},
					},
					queryId: 2,
				},
			},
		]);
	} else if (after < 9000) {
		return HttpResponse.json<Message[]>([
			{
				id: 3,
				timestamp: 9000,
				senderName: "Gustave",
				content: {
					type: "image",
					imageDataURI: "data/png;asdakwdkjn",
				},
			},
		]);
	} else {
		return HttpResponse.json<Message[]>([]);
	}
});

export const handlers = [
	// This is an HTTP long poll for agent messages sent after a given timestamp
	http.get("/api/exchanges/:id/messages", getMessagesHandler),
];
