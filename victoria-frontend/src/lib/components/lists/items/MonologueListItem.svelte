<script lang="ts">
	import MonologueStatusIndicator from "$lib/components/indicators/MonologueStatusIndicator.svelte";
	import {
		type MonologueListItem,
		type Monologue,
		MonologueStatusEvent,
	} from "$lib/types/monologue";
	import { goto } from "$app/navigation";
	import type { Subscription } from "$lib/types/websocket";
	import Subscriber from "$lib/components/placeholders/Subscriber.svelte";

	function openMonologueDetail() {
		goto(`/monologues/${monologue.id}`);
	}

	export let monologue: MonologueListItem | Monologue;
	let subscription: Subscription = {
		type: "monologue_status",
		monologueId: monologue.id,
		sendInitial: false,
	};

	function handler(msg: any) {
		let e = MonologueStatusEvent.safeParse(msg);

		if (e.success) {
			monologue = e.data.monologue;
		}
	}
</script>

<button
	on:click={openMonologueDetail}
	class="flex flex-row px-2 my-1 border-t-2 border-black hover:bg-slate-400"
>
	<Subscriber {handler} {subscription}>
		<div class="content-center">
			<MonologueStatusIndicator
				status={monologue.status}
				startTimestamp={monologue.startTimestamp}
			/>
		</div>
		<div class="grow mx-2 min-w-0 flex flex-col">
			<div class="font-bold">
				{monologue.title}
			</div>
			<div>
				{monologue.summary}
			</div>
		</div>
	</Subscriber>
</button>
