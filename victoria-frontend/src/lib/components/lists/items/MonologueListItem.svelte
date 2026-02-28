<script lang="ts">
	import MonologueStatusIndicator from "$lib/components/indicators/MonologueStatusIndicator.svelte";
	import type { Agent } from "$lib/types/agent";
	import type { MonologueListItem } from "$lib/types/monologue";
	import { goto } from "$app/navigation";
	import { onMount } from "svelte";
	import { getAgent } from "$lib/api/agents";
	import Loader from "$lib/components/placeholders/Loader.svelte";

	function openMonologueDetail() {
		goto(`/monologues/${monologue.id}`);
	}

	export let monologue: MonologueListItem;
	let agent: Agent | null = null;

	let agentPromise: Promise<any> = Promise.resolve();

	async function loadAgent() {
		agent = await getAgent(monologue.agentId);
	}

	onMount(() => {
		agentPromise = loadAgent();
	});
</script>

<button
	on:click={openMonologueDetail}
	class="flex flex-row px-2 my-1 border-t-2 border-black hover:bg-slate-400"
>
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

		<div>
			<Loader
				promise={agentPromise}
				pendingMessage="Loading agent info..."
				rejectMessage="Failed to load agent info"
			>
				Started by <span class="font-semibold text-blue-500"
					>{agent?.name}</span
				> 20m ago
			</Loader>
		</div>
	</div>
</button>

