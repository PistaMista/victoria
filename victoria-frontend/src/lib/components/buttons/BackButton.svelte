<script lang="ts">
	import { ChevronLeftOutline } from "flowbite-svelte-icons";
	import { goto } from "$app/navigation";

	export let route: string;
</script>

<button
	on:click={() => goto(route)}
	class="flex flex-row hover:bg-slate-500 rounded-md p-1"
>
	<ChevronLeftOutline class="h-8 w-8 my-auto" />
	<div class="content-center mr-2">Back</div>
</button>

