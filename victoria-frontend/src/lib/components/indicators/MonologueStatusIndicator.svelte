<script lang="ts">
	import {
		ClockOutline,
		RocketOutline,
		CheckOutline,
	} from "flowbite-svelte-icons";
	import type { MonologueStatus } from "$lib/types/monologue";
	import { Duration, DateTime } from "ts-luxon";
	import { onMount } from "svelte";

	export let horizontal: Boolean = false;

	export let status: MonologueStatus;
	export let startTimestamp: number = Date.now();
	export let endTimestamp: number | null = null;

	export let displayRuntime: Boolean = false;
	export let displayStartDate: Boolean = false;
	export let displayEndDate: Boolean = false;

	const colors = {
		RUNNING: "blue-500",
		PENDING: "orange-500",
		SUCCESS: "lime-500",
		FAILURE: "red-500",
	};

	let currentTime: number = Date.now();
	let runtime: number = 0;

	$: duration = Duration.fromMillis(runtime).shiftTo("minutes", "seconds");
	$: startDate = DateTime.fromSeconds(startTimestamp);
	$: endDate = endTimestamp ? DateTime.fromSeconds(endTimestamp) : null;

	$: if (endTimestamp === null) {
		runtime = currentTime - startTimestamp;
	} else {
		runtime = endTimestamp - startTimestamp;
	}

	function tickTime() {
		currentTime = Date.now();
	}

	onMount(() => {
		const interval = setInterval(tickTime, 1000);
		return () => clearInterval(interval);
	});
</script>

<div class="flex flex-{horizontal ? 'row' : 'col'}">
	<div class="bg-black rounded-md px-1 font-bold text-{colors[status]}">
		{status}
	</div>
	<div class="grow" />

	{#if displayRuntime}
		<div class="p-1 flex flex-row">
			<ClockOutline />
			{Math.floor(duration.minutes)}m{Math.floor(duration.seconds)}s
		</div>
	{/if}

	{#if displayStartDate}
		<div class="p-1 border-l-2 flex flex-row">
			<RocketOutline />
			{startDate.toLocal().toFormat("yyyy/MM/dd HH:mm")}
		</div>
	{/if}

	{#if displayEndDate && endDate}
		<div class="p-1 border-l-2 flex flex-row">
			<CheckOutline />
			{#if status === "SUCCESS" || status === "FAILURE"}
				{endDate.toLocal().toFormat("yyyy/MM/dd HH:mm")}
			{:else}
				N/A
			{/if}
		</div>
	{/if}
</div>

