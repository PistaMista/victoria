<script lang="ts">
	import ListViewHeaderButton from "$lib/components/buttons/ListViewHeaderButton.svelte";
	import AgentCard from "$lib/components/cards/AgentCard.svelte";
	import ListViewHeaderSearchBar from "$lib/components/search/ListViewHeaderSearchBar.svelte";
	import ListView from "$lib/views/ListView.svelte";
	import { PlusOutline } from "flowbite-svelte-icons";
	import type { AgentListItem } from "$lib/types/agent";
	import Loader from "$lib/components/placeholders/Loader.svelte";
	import { goto } from "$app/navigation";
	import { onMount } from "svelte";
	import { getCurrentUserAgents } from "$lib/api/agents";

	let agents: AgentListItem[] = [];
	let searchQuery: string = "";
	let mounted = false;

	let dataPromise: Promise<void> = Promise.resolve();

	function createAgent() {
		goto("/agents/add");
	}

	onMount(() => {
		mounted = true;
	});

	$: if (mounted) {
		dataPromise = (async () => {
			let query: string | null = searchQuery ? searchQuery : null;
			agents = await getCurrentUserAgents(query);
		})();
	}
</script>

<ListView cards>
	<svelte:fragment slot="header">
		<ListViewHeaderSearchBar
			ontype={(val) => {
				searchQuery = val;
			}}
		/>
		<div class="mx-2 content-center flex flex-row">
			<ListViewHeaderButton
				onclick={createAgent}
				aria-label="Create agent"
				><PlusOutline class="w-6 h-6" /></ListViewHeaderButton
			>
		</div>
	</svelte:fragment>

	<svelte:fragment slot="items">
		<Loader
			promise={dataPromise}
			pendingMessage="Loading agents..."
			rejectMessage="Failed to load agents"
		>
			{#each agents as agent}
				<AgentCard {agent} />
			{/each}
		</Loader>
	</svelte:fragment>
</ListView>

