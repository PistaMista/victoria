<script lang="ts">
	import { CloseOutline } from "flowbite-svelte-icons";
	import { socketStatus } from "$lib/api/websocket";
</script>

{#if !$socketStatus.connected}
	<div class="flex flex-row text-red-500 font-bold justify-center">
		<CloseOutline class="mr-2" />
		Connection lost, reconnecting... (attempt {$socketStatus.reconnectAttemptIdx})
	</div>
{/if}
