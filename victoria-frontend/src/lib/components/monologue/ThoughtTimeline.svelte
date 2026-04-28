<script lang="ts">
	import { ThoughtListingEvent, type Thought } from "$lib/types/thought";
	import ItemComponent from "./Thought.svelte";
	import Subscriber from "../placeholders/Subscriber.svelte";
	import type { Subscription } from "$lib/types/websocket";

	export let monologueId: number;

	let thoughts: Thought[] = [];
	let subscription: Subscription = {
		type: "monologue_thoughts",
		monologueId: monologueId,
	};

	function handler(msg: any) {
		let e = ThoughtListingEvent.safeParse(msg);

		if (e.success) {
			switch (e.data.type) {
				case "initial":
					thoughts = e.data.thoughts;
					break;
				case "new":
					thoughts = [...thoughts, e.data.thought];
					break;
			}
		}
	}
</script>

<Subscriber {subscription} {handler}>
	<div class="relative flex flex-col px-2 py-2 space-y-12">
		{#each thoughts as thought}
			<ItemComponent {thought} />
		{/each}

		<!-- Dotted line for decoration-->
		<div
			class="absolute z-10 top-0 bottom-4 left-6 w-0.5 border-l-4 border-dotted border-gray-200"
		/>
	</div>
</Subscriber>
