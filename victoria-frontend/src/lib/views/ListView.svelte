<script lang="ts">
	import BackButton from "$lib/components/buttons/BackButton.svelte";

	export let cards: Boolean = false;
	export let backRoute: string | null = null;
</script>

<!-- Must support both a pure list view (items in a column) and a flex-wrap layout with cards -->
<!-- There should be an option to either include or not include a back button -->

<div class="flex flex-col w-full h-full">
	<div class="p-1 bg-slate-400 flex flex-col md:flex-row">
		{#if backRoute}
			<BackButton route={backRoute} />
		{/if}
		<slot name="header" />
	</div>

	{#if cards}
		<div
			role="list"
			class="flex flex-col md:flex-row md:flex-wrap justify-start p-2"
		>
			<slot name="items" />
		</div>
	{:else}
		<div
			role="list"
			class="flex flex-col grow min-h-0 bg-slate-300 overflow-y-scroll"
		>
			<slot name="items" />
		</div>
	{/if}
</div>

