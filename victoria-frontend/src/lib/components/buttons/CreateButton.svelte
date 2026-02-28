<script lang="ts">
	import { Button } from "flowbite-svelte";
	import { PlusOutline } from "flowbite-svelte-icons";

	export let onclick: () => void;
</script>

<Button on:click={onclick} class="w-full font-bold bg-lime-600" {...$$restProps}
	><PlusOutline />CREATE</Button
>

