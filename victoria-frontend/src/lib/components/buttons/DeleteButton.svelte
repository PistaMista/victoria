<script lang="ts">
	import { Button, Modal } from "flowbite-svelte";
	import { TrashBinSolid } from "flowbite-svelte-icons";

	export let onclick: () => void;

	let menuShown: boolean = false;

	function showMenu() {
		menuShown = true;
	}

	function hideMenu() {
		menuShown = false;
	}
</script>

<Button on:click={showMenu} class="w-full font-bold bg-red-600" {...$$restProps}
	><TrashBinSolid />DELETE</Button
>

{#if menuShown}
	<Modal bind:open={menuShown}>
		<div class="text-center">
			<TrashBinSolid class="mx-auto h-12 w-12" />
			<h3>Are you sure you want to delete this?</h3>
			<Button
				aria-label="Cancel"
				on:click={hideMenu}
				class="ml-auto font-bold bg-blue-600">Cancel</Button
			>
			<Button
				aria-label="Delete"
				on:click={onclick}
				class="mr-auto font-bold bg-red-600">DELETE</Button
			>
		</div>
	</Modal>
{/if}
