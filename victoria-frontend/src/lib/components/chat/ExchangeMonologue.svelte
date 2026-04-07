<script lang="ts">
	import { goto } from "$app/navigation";
	import { MonologueStatusEvent } from "$lib/types/monologue";
	import type { Monologue } from "$lib/types/monologue";
	import type { Subscription } from "$lib/types/websocket";
	import MonologueStatusIndicator from "$lib/components/indicators/MonologueStatusIndicator.svelte";
	import Subscriber from "$lib/components/placeholders/Subscriber.svelte";

	export let monologueId: number;

	let monologue: Monologue | null = null;
	let subscription: Subscription = {
		type: "monologue_status",
		monologueId: monologueId,
	};

	function handler(msg: any) {
		let e = MonologueStatusEvent.safeParse(msg);

		if (e.success) {
			monologue = e.data.monologue;
		}
	}
</script>

<div class="flex flex-row mt-1">
	<Subscriber {subscription} {handler}>
		{#if monologue}
			<a
				aria-label="Go to monologue"
				class="font-semibold hover:text-blue-500"
				on:click={() => goto(`/monologues/${monologue?.id}`)}
				href={`/monologues/${monologue.id}`}
				>{monologue.title}</a
			>
			<div class="ml-auto">
				<MonologueStatusIndicator
					horizontal
					status={monologue.status}
					startTimestamp={monologue.startTimestamp}
					endTimestamp={monologue.endTimestamp}
					displayRuntime
				/>
			</div>
		{:else}
			<div class="font-semibold text-red-500">
				MONOLOGUE UNAVAILABLE
			</div>
		{/if}
	</Subscriber>
</div>
