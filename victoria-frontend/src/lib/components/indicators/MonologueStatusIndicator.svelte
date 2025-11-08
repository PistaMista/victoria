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
	export let startTimestamp: number = 0;
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

	let currentDate: DateTime = DateTime.now().toUTC();
	let runtime: Duration = Duration.fromMillis(0);

	$: duration = runtime.shiftTo("minutes", "seconds");
	$: startDate = DateTime.fromSeconds(startTimestamp, {
		zone: "utc",
	}).toUTC();
	$: endDate = endTimestamp
		? DateTime.fromSeconds(endTimestamp, { zone: "utc" }).toUTC()
		: null;

	$: if (endDate === null) {
		runtime = currentDate.diff(startDate);
	} else {
		runtime = endDate.diff(startDate);
	}

	function tickTime() {
		currentDate = DateTime.now().toUTC();
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
