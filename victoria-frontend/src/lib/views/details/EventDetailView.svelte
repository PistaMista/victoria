<script lang="ts">
	import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
	import DetailView from "$lib/views/DetailView.svelte";
	import { onMount } from "svelte";
	import type { Event } from "$lib/types/event";
	import { getEvent } from "$lib/api/events";
	import { getTrigger } from "$lib/api/triggers";
	import Loader from "$lib/components/placeholders/Loader.svelte";

	export let id: number;

	let loadedEvent: Event = {
		triggerId: 0,
		content: "None",
	};
	let triggerName: string = "";

	let dataPromise: Promise<any> = Promise.resolve();

	async function load() {
		loadedEvent = await getEvent(id);
		triggerName = (await getTrigger(loadedEvent.triggerId)).name;
	}

	onMount(async () => {
		dataPromise = load();
	});
</script>

<Loader
	promise={dataPromise}
	pendingMessage="Loading event..."
	rejectMessage="Failed to load event"
>
	<DetailView>
		<DetailViewSection title="Trigger">
			{triggerName}
		</DetailViewSection>

		<DetailViewSection title="Content">
			{loadedEvent.content}
		</DetailViewSection>
	</DetailView>
</Loader>

