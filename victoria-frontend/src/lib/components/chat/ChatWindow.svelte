<script lang="ts">
	import ItemComponent from "./Exchange.svelte";
	import Subscriber from "$lib/components/placeholders/Subscriber.svelte";
	import { ExchangeListingEvent } from "$lib/types/exchange";
	import type { Exchange } from "$lib/types/exchange";
	import type { Subscription } from "$lib/types/websocket";

	export let id: number;

	let exchanges: Exchange[] = [];
	let subscription: Subscription = { type: "chat_exchanges", chatId: id };

	function handler(content: any) {
		let e = ExchangeListingEvent.safeParse(content);

		if (e.success) {
			switch (e.data.type) {
				case "initial":
					exchanges = e.data.exchanges;
					break;
				case "new":
					exchanges = [...exchanges, e.data.exchange];
					break;
			}
		}
	}
</script>

<Subscriber {subscription} {handler}>
	<div class="grow min-h-0 mb-2 overflow-y-scroll">
		<div class="flex flex-col md:w-2/3 mx-2 md:m-auto">
			{#each exchanges as exchange, i}
				<ItemComponent
					{exchange}
					latest={i === exchanges.length - 1}
				/>
			{/each}
		</div>
	</div>
</Subscriber>
