import { delay, http, HttpResponse } from "msw";
import { ChatOptions, type Chat, type SentMessageInfo } from "$lib/types/chat";
import { spy } from "../spy";
import type { Exchange } from "$lib/types/exchange";

export const listChatsHandler = await spy(({ request }) => {
	const url = new URL(request.url);
	const sortBy = url.searchParams.get("sortBy");
	const receiver = url.searchParams.get("receiver");

	const chats = {
		admin: {
			id: 1,
			title: "System admin",
			summary: "Chat about system administration.",
		},
		learning: {
			id: 2,
			title: "Language learning",
			summary: "Discussing ways to learn languages effectively.",
		},
	};

	switch (receiver) {
		case "general":
			return HttpResponse.json<Array<Chat>>([chats.admin]);

		case "research":
			return HttpResponse.json<Array<Chat>>([chats.learning]);
	}

	switch (sortBy) {
		case "importance":
			return HttpResponse.json<Array<Chat>>([chats.learning, chats.admin]);
		case "length":
		case "recent":
			return HttpResponse.json<Array<Chat>>([chats.admin, chats.learning]);
	}
});

export const getChatHandler = await spy(({ request: { id } }) => {
	return HttpResponse.json<Chat>({
		id: Number(id),
		title: "System admin",
		summary: "A chat about system administration",
	});
});

export const chatCreateHandler = await spy(() => {
	return HttpResponse.json<Chat>({
		id: 3,
		title: "New chat",
		summary: "A chat about nothing in particular (yet).",
	});
});

export const duplicateChatHandler = await spy(
	// This accepts the "toExchange: id" parameter in the body,
	// which duplicates the chat only up to the given exchange
	() => {
		return HttpResponse.json<number>(3);
	},
);

export const chatDeleteHandler = await spy(() => {
	return HttpResponse.json<Boolean>(true);
});

export const sendMessageHandler = await spy(() => {
	return HttpResponse.json<SentMessageInfo>({
		exchangeId: 3,
	});
});

export const getExchangesHandler = await spy(async ({ request }) => {
	let url: URL = new URL(request.url);
	let after: number = Number(url.searchParams.get("after"));

	await delay(400);

	if (after < 2500) {
		return HttpResponse.json<Exchange[]>([
			{
				id: 2,
				chatId: 1,
				timestamp: 2500,
				userMessage: {
					id: 2,
					senderName: "Krystof",
					timestamp: 2405,
					content: {
						type: "markdown",
						markdownText: "Hmmm, *yeees*",
					},
				},
				monologueIds: [1, 2],
			},
			{
				id: 3,
				chatId: 1,
				timestamp: 2700,
				userMessage: {
					id: 2,
					senderName: "Krystof",
					timestamp: 2405,
					content: {
						type: "markdown",
						markdownText: "Hello?",
					},
				},
				monologueIds: [1, 2],
			},
		]);
	} else if (after < 3300) {
		return HttpResponse.json<Exchange[]>([
			{
				id: 3,
				chatId: 1,
				timestamp: 3300,
				userMessage: {
					id: 2,
					senderName: "Krystof",
					timestamp: 2405,
					content: {
						type: "markdown",
						markdownText: "Goodbye.",
					},
				},
				monologueIds: [1, 2],
			},
		]);
	} else {
		return HttpResponse.json<Exchange[]>([]);
	}
});

export const getChatOptionsHandler = await spy(() => {
	return HttpResponse.json<ChatOptions>({
		receiver: "general",
		enabledActionIds: [1, 3],
	});
});

export const setChatOptionsHandler = await spy(() => {
	return HttpResponse.json<ChatOptions>({
		receiver: "research",
		enabledActionIds: [1, 4],
	});
});

export const listChatReceiversHandler = await spy(() => {
	return HttpResponse.json<string[]>(["general", "research"]);
});

export const handlers = [
	http.get("/api/chats", listChatsHandler),
	http.post("/api/chats", chatCreateHandler),
	http.delete("/api/chats/:id", chatDeleteHandler),

	http.get("/api/chats/receivers", listChatReceiversHandler),

	// This duplicates a chat
	http.post("/api/chats/:id/duplicate", duplicateChatHandler),

	// This returns the ID of the created exchange
	http.post("/api/chats/:id/send-message", sendMessageHandler),

	// This is a long-poll endpoint to get exchanges created after a certain time
	http.get("/api/chats/:id/exchanges", getExchangesHandler),

	http.get("/api/chats/:id/options", getChatOptionsHandler),
	http.put("/api/chats/:id/options", setChatOptionsHandler),

	http.get("/api/chats/:id", getChatHandler),
];
