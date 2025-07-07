<script lang="ts">
    import { Button } from "flowbite-svelte";
    import { TrashBinSolid } from "flowbite-svelte-icons";

    export let onclick: () => void;
</script>

<Button on:click={onclick} class="w-full font-bold bg-red-600"><TrashBinSolid/>DELETE</Button>