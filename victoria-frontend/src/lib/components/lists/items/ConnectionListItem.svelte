<script lang="ts">
	import type { ConnectionListItem } from "$lib/types/connection";
	import { Button } from "flowbite-svelte";
	import { CogSolid } from "flowbite-svelte-icons";
	import { goto } from "$app/navigation";

	export let connection: ConnectionListItem;
</script>

<div class="flex flex-row">
	<div class="mr-auto">{connection.name}</div>
	<Button
		on:click={() => {
			goto(`/admin/settings/connections/${connection.id}/edit`);
		}}
		class="w-6 h-6 p-0"><CogSolid /></Button
	>
</div>

