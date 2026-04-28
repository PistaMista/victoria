<script lang="ts">
	import { onDestroy } from "svelte";
	import type { Writable } from "svelte/store";
	import { CloseOutline } from "flowbite-svelte-icons";
	import { Spinner } from "flowbite-svelte";
	import type {
		Subscription,
		EventHandler,
		HandlerSubscription,
	} from "$lib/types/websocket";
	import { SubscriptionState } from "$lib/types/websocket";
	import { subscribeEvent } from "$lib/api/websocket";

	export let subscription: Subscription;
	export let handler: EventHandler;

	let subscribed: Writable<HandlerSubscription> = subscribeEvent(
		subscription,
		handler,
	);

	onDestroy(() => {
		$subscribed.unsubscribeHandle();
	});
</script>

{#if $subscribed.state === SubscriptionState.Subscribing}
	<div class="mx-auto my-2">
		<div>
			<div
				class="flex flex-row text-yellow-700 font-bold justify-center"
			>
				<Spinner color="yellow" class="mr-2" />
				Connecting...
			</div>
		</div>
	</div>
{:else if $subscribed.state === SubscriptionState.Subscribed}
	<slot />
{:else if $subscribed.state === SubscriptionState.Cancelling}
	<div class="mx-auto my-2">
		<div>
			<div
				class="flex flex-row text-red-700 font-bold justify-center"
			>
				<Spinner color="red" class="mr-2" />
				Disconnecting...
			</div>
		</div>
	</div>
{:else if $subscribed.state === SubscriptionState.Cancelled}
	<div class="mx-auto my-2">
		<div>
			<div
				class="flex flex-row text-red-500 font-bold justify-center"
			>
				<CloseOutline class="mr-2" />
				Disconnected.
			</div>
			<div class="text-red-500">
				{$subscribed.cancelReason}
			</div>
		</div>
	</div>
{/if}
