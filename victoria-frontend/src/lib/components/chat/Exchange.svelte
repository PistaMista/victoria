<script lang="ts">
	import ItemComponent from "./Message.svelte";
	import MonologueStatusIndicator from "../indicators/MonologueStatusIndicator.svelte";
	import { writable, type Writable } from "svelte/store";
	import { ShareAllOutline } from "flowbite-svelte-icons";
	import type { Exchange } from "$lib/types/exchange";
	import type { Message } from "$lib/types/message";
	import { onDestroy, onMount } from "svelte";
	import {
		duplicateChatToExchange,
		startReceivingMessages,
	} from "$lib/api/chatting";
	import ExchangeContextButton from "../buttons/ExchangeContextButton.svelte";
	import type { Monologue } from "$lib/types/monologue";
	import { getMonologue } from "$lib/api/monologues";
	import { goto } from "$app/navigation";
	import Loader from "../placeholders/Loader.svelte";

	export let exchange: Exchange;

	let agentMessages: Writable<Message[]> = writable([]);
	let monologues: Monologue[] = [];

	let abortController: AbortController = new AbortController();

	let receivePromise: Promise<any> = Promise.resolve();
	let getMonologuesPromise: Promise<any> = Promise.resolve();
	let createNewChatPromise: Promise<any> = Promise.resolve();

	async function loadMonologues() {
		monologues = await Promise.all(
			exchange.monologueIds.map((id) => getMonologue(id)),
		);
	}

	function createNewChatFromHere() {
		createNewChatPromise = duplicateChatToExchange(
			exchange.chatId,
			exchange.id,
		);
	}

	onMount(() => {
		getMonologuesPromise = loadMonologues();
		receivePromise = startReceivingMessages(
			exchange.id,
			agentMessages,
			abortController.signal,
		);
	});

	onDestroy(() => {
		abortController.abort("Exchange component destroyed");
	});
</script>

{#await receivePromise}
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
			{#each $agentMessages as message}
				<ItemComponent {message} />
			{/each}
		</div>
		<!-- Running monologue info -->
		<Loader
			promise={getMonologuesPromise}
			pendingMessage="Fetching monologues..."
			rejectMessage="Failed to get monologues"
		>
			<div class="flex flex-col space-y-2">
				{#each monologues as monologue}
					<div class="flex flex-row mt-1">
						<a
							aria-label="Go to monologue"
							class="font-semibold hover:text-blue-500"
							on:click={() =>
								goto(
									`/monologues/${monologue.id}`,
								)}
							href={`/monologues/${monologue.id}`}
							>{monologue.title}</a
						>
						<div class="ml-auto">
							<MonologueStatusIndicator
								horizontal
								status={monologue.status}
								startTimestamp={monologue.startTimestamp}
								displayRuntime
							/>
						</div>
					</div>
				{/each}
			</div>
		</Loader>
		<!-- These buttons are only shown if there is no Exchange at this level with a non-completed Monologue -->
		<!-- Use ExchangeContextButton here -->
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
{:catch}
	<Loader
		promise={receivePromise}
		pendingMessage="Receiving messages..."
		rejectMessage="Failure while receiving messages"
	/>
{/await}

