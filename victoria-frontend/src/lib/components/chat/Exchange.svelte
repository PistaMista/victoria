<script lang="ts">
	import ItemComponent from "./Message.svelte";
	import ExchangeMonologue from "./ExchangeMonologue.svelte";
	import { ShareAllOutline } from "flowbite-svelte-icons";
	import type { Exchange } from "$lib/types/exchange";
	import { MessageListingEvent } from "$lib/types/message";
	import type { Message } from "$lib/types/message";
	import { duplicateChatToExchange } from "$lib/api/chatting";
	import ExchangeContextButton from "../buttons/ExchangeContextButton.svelte";
	import type { Subscription } from "$lib/types/websocket";
	import Subscriber from "$lib/components/placeholders/Subscriber.svelte";
	import Loader from "../placeholders/Loader.svelte";

	export let exchange: Exchange;
	export let latest = false;

	let agentMessages: Message[] = [];

	let createNewChatPromise: Promise<any> = Promise.resolve();

	let subscription: Subscription = {
		type: "exchange_agent_messages",
		exchangeId: exchange.id,
	};

	function handler(content: any) {
		let e = MessageListingEvent.safeParse(content);

		if (e.success) {
			switch (e.data.type) {
				case "initial":
					agentMessages = e.data.messages;
					break;
				case "new":
					agentMessages = [
						...agentMessages,
						e.data.message,
					];
					break;
			}
		}
	}

	function createNewChatFromHere() {
		createNewChatPromise = duplicateChatToExchange(
			exchange.chatId,
			exchange.id,
		);
	}
</script>

<div class="w-full flex flex-col">
	<!-- This is the user's Message -->
	{#if exchange.userMessage !== null}
		<div
			class="border-b-2 border-slate-500 bg-orange-200 rounded-t-md p-1"
		>
			<ItemComponent message={exchange.userMessage} />
		</div>
	{/if}
	<!-- These are the Message(s) sent by the Agent -->
	<div
		class="{exchange.userMessage
			? ''
			: 'rounded-t-md'} flex flex-col space-y-2 border-b-2 border-slate-500 border-dashed bg-slate-100 p-1"
	>
		<Subscriber {subscription} {handler}>
			{#each agentMessages as message}
				<ItemComponent {message} />
			{/each}
		</Subscriber>
	</div>
	<!-- Running monologue info -->
	<div class="flex flex-col space-y-2">
		{#each exchange.monologueIds as monologueId}
			<ExchangeMonologue {monologueId} />
		{/each}
	</div>
	<!-- These buttons are only shown if there is no Exchange at this level with a non-completed Monologue -->
	<Loader
		promise={createNewChatPromise}
		pendingMessage="Creating new chat from here"
		rejectMessage="Failed to create new chat"
	>
		<div class="flex flex-row mt-1 space-x-1 content-center">
			<ExchangeContextButton
				onclick={createNewChatFromHere}
				aria-label="Create new chat from here"
			>
				<ShareAllOutline />
			</ExchangeContextButton>
		</div>
	</Loader>
</div>
