<script lang="ts" context="module">
	export type Option = {
		displayName: string;
		ariaLabel: string;
		value: any;
	};
</script>

<script lang="ts">
	import { Dropdown, DropdownItem } from "flowbite-svelte";
	import { ChevronDownOutline, CheckOutline } from "flowbite-svelte-icons";

	export let options: Option[];
	export let chosenOption: Option | null = null;
	export let title: string;

	function chooseOption(option: Option) {
		chosenOption = option;
	}
</script>

<div class="hover:bg-slate-300 rounded-md" {...$$restProps}>
	<button class="flex flex-row p-1 m-1"
		>{title}<ChevronDownOutline class="w-6 h-6" /></button
	>
	<Dropdown>
		{#each options as option}
			<DropdownItem
				aria-label={option.ariaLabel}
				on:click={() => chooseOption(option)}
			>
				{option.displayName}
				{#if option === chosenOption}
					<CheckOutline />
				{/if}
			</DropdownItem>
		{/each}
	</Dropdown>
</div>
