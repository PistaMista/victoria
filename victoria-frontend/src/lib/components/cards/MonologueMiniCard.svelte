<script lang="ts">
	import {
		ClockOutline,
		CheckCircleOutline,
		CloseCircleOutline,
		ExclamationCircleOutline,
	} from "flowbite-svelte-icons";
	import {
		MonologueStatusEvent,
		type Monologue,
	} from "$lib/types/monologue";
	import { goto } from "$app/navigation";
	import Subscriber from "$lib/components/placeholders/Subscriber.svelte";
	import type { Subscription } from "$lib/types/websocket";

	export let monologueId: number;
	let monologue: Monologue | null = null;
	let subscription: Subscription = {
		type: "monologue_status",
		sendInitial: true,
		monologueId: monologueId,
	};

	function handler(msg: any) {
		let e = MonologueStatusEvent.safeParse(msg);

		if (e.success) {
			monologue = e.data.monologue;
		}
	}

	function goToDetail() {
		goto(`/monologues/${monologueId}`);
	}
</script>

<button on:click={goToDetail} class="flex bg-slate-400 p-1 rounded-md">
	<Subscriber {subscription} {handler}>
		{#if monologue}
			{monologue.title}
			<div class="grow mx-2" />

			{#if monologue.status === "PENDING"}
				<ExclamationCircleOutline />
			{:else if monologue.status === "RUNNING"}
				<ClockOutline />
			{:else if monologue.status === "SUCCESS"}
				<CheckCircleOutline />
			{:else if monologue.status === "FAILURE"}
				<CloseCircleOutline />
			{/if}
		{:else}
			MONOLOGUE UNAVAILABLE
		{/if}
	</Subscriber>
</button>
