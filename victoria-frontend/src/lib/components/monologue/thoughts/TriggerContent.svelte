<script lang="ts">
	import { RocketSolid } from "flowbite-svelte-icons";
	import type { TriggerInvocation } from "$lib/types/thought";
	import type { Event } from "$lib/types/event";
	import { onMount } from "svelte";
	import { getEvent } from "$lib/api/events";
	import { getTrigger } from "$lib/api/triggers";
	import { goto } from "$app/navigation";
	import Loader from "$lib/components/placeholders/Loader.svelte";

	export let content: TriggerInvocation;

	let triggerName: string = "";

	let dataPromise: Promise<any> = Promise.resolve();

	async function load() {
		let event: Event = await getEvent(content.parameters.eventId);
		triggerName = (await getTrigger(event.triggerId)).name;
	}

	onMount(() => {
		dataPromise = load();
	});
</script>

<Loader
	promise={dataPromise}
	pendingMessage="Loading trigger info..."
	rejectMessage="Failed to load trigger info"
>
	<div>
		<RocketSolid class="float-left mr-2" />
		<!-- This will be a link to the detail of the event -->
		<button
			on:click={() => goto(`/events/${content.parameters.eventId}`)}
			class="w-full font-semibold"
			aria-label="Go to triggering event">{triggerName}</button
		>
	</div>
</Loader>

