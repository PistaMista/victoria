<script lang="ts">
	import { Label, Range, Input, Button } from "flowbite-svelte";
	import { RefreshOutline } from "flowbite-svelte-icons";
	import { clamp } from "$lib/util/math";

	export let label: string;

	export let fallback: number;
	export let value: number;
	export let max: number;
	export let min: number;

	$: newValue = value;
</script>

<div class="flex flex-row mt-2">
	<div class="grow flex flex-col">
		<Label>{label}</Label>
		<Range bind:value {max} {min} class="place-self-center ml-1 grow" />
	</div>

	<form on:submit={() => (value = clamp(newValue, min, max))}>
		<Input
			{...$$restProps}
			bind:value={newValue}
			on:blur={() => (newValue = value)}
			class="place-self-center ml-1 w-12"
		/>
	</form>
	<Button on:click={() => (value = fallback)} class="p-1 ml-1"
		><RefreshOutline></RefreshOutline></Button
	>
</div>

