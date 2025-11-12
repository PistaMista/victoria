import type { ChatOptions, Chat, SentMessageInfo } from "$lib/types/chat";
import { Chat as ChatSchema, ChatOptions as ChatOptionsSchema, SentMessageInfo as SentMessageInfoSchema } from "$lib/types/chat";
import type { Diff } from "$lib/types/diff";
import type { Exchange } from "$lib/types/exchange";
import { Exchange as ExchangeSchema } from "$lib/types/exchange";
import { z } from "zod";
import { get, type Writable } from "svelte/store";
import { type Message, Message as MessageSchema } from "$lib/types/message";

export type SortMode = 'recent' | 'length' | 'importance';

export async function getCurrentUserChats(sortBy: SortMode = 'recent', receiver: string | null = null, searchQuery: string | null = null): Promise<Chat[]> {
	const params = new URLSearchParams({
		sortBy: sortBy
	});

	if (receiver) {
		params.append("receiver", receiver);
	}

	if (searchQuery) {
		params.append("searchQuery", searchQuery);
	}

	const res = await fetch(`/api/chats?${params.toString()}`, {
		method: 'GET'
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return z.array(ChatSchema).parse(json);
}

export async function getChatReceivers(): Promise<string[]> {
	const res = await fetch('/api/chats/receivers', {
		method: 'GET'
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return z.array(z.string()).parse(json);
}

export async function createNewChat(): Promise<Chat> {
	const res = await fetch('/api/chats', { method: 'POST' });
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return ChatSchema.parse(json);
}

export async function deleteChat(id: number): Promise<void> {
	const res = await fetch(`/api/chats/${id}`, { method: 'DELETE' });
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}
}

export async function getChatOptions(id: number): Promise<ChatOptions> {
	const res = await fetch(`/api/chats/${id}/options`, { method: 'GET' });
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return ChatOptionsSchema.parse(json);
}

export async function updateChatOptions(id: number, changes: Diff<ChatOptions>): Promise<void> {
	const res = await fetch(`/api/chats/${id}/options`, {
		method: 'PUT',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(changes)
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}
}

export async function sendMessageToChat(chatId: number, msg: string): Promise<SentMessageInfo> {
	const res = await fetch(`/api/chats/${chatId}/send-message`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ type: "markdown", message: msg })
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return SentMessageInfoSchema.parse(json);
}

export async function startReceivingExchanges(chatId: number, out: Writable<Exchange[]>, abortSig: AbortSignal): Promise<void> {
	let fetcher = (async () => {
		const maxTimestamp = get(out).map((val) => (val.timestamp)).reduce((a, b) => Math.max(a, b), 0);
		const params = new URLSearchParams({
			after: maxTimestamp.toString()
		})
		const res = await fetch(`/api/chats/${chatId}/exchanges?${params.toString()}`, {
			method: 'GET',
			signal: abortSig
		});
		const json = await res.json();

		if (!res.ok) {
			throw Error(json.detail);
		}

		const exchanges = z.array(ExchangeSchema).parse(json);
		out.update(prev => [...prev, ...exchanges]);
	});

	let loop: Promise<void> = (async () => {
		while (!abortSig.aborted) {
			await fetcher();
		}
	})();

	return loop;
}

export async function startReceivingMessages(exchangeId: number, out: Writable<Message[]>, once: boolean, abortSig: AbortSignal): Promise<void> {
	let fetcher = (async () => {
		const maxTimestamp = get(out).map((val) => (val.timestamp)).reduce((a, b) => Math.max(a, b), 0);
		const params = new URLSearchParams({
			after: maxTimestamp.toString()
		})
		const res = await fetch(`/api/exchanges/${exchangeId}/messages?${params.toString()}`, {
			method: 'GET',
			signal: abortSig
		});
		const json = await res.json();

		if (!res.ok) {
			throw Error(json.detail);
		}

		const messages = z.array(MessageSchema).parse(json);
		out.update(prev => [...prev, ...messages]);
	});

	let loop: Promise<void> = (async () => {
		while (!abortSig.aborted) {
			await fetcher();

			if (once) {
				break;
			}
		}
	})();

	return loop;
}

export async function duplicateChatToExchange(chatId: number, exchangeId: number): Promise<number> {
	const res = await fetch(`/api/chats/${chatId}/duplicate`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			toExchange: exchangeId
		})
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return z.number().parse(json);
}
