<script lang="ts" context="module">
	export type Option = {
		displayName: string;
		ariaLabel: string;
		value: any;
	};
</script>

<script lang="ts">
	import { Button, Dropdown, DropdownItem } from "flowbite-svelte";
	import { ChevronDownOutline } from "flowbite-svelte-icons";

	export let options: Option[];
	export let chosenOption: Option | null = null;
	export let placeholder: string;

	let dropdownOpen: boolean = false;

	function chooseOption(option: Option) {
		chosenOption = option;
		dropdownOpen = false;
	}
</script>

<div {...$$restProps}>
	<Button class="flex flex-row w-full"
		>{chosenOption?.displayName ?? placeholder}<ChevronDownOutline
			class="w-6 h-6"
		/></Button
	>
	<Dropdown bind:open={dropdownOpen}>
		{#each options as option}
			<DropdownItem
				aria-label={option.ariaLabel}
				on:click={() => chooseOption(option)}
			>
				{option.displayName}
			</DropdownItem>
		{/each}
	</Dropdown>
</div>
