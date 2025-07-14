<script lang="ts">
    import { Button } from "flowbite-svelte";
    import { FloppyDiskSolid } from "flowbite-svelte-icons";
    
    export let onclick: () => void;
</script>

<Button on:click={onclick} class="w-full font-bold bg-blue-600" {...$$restProps}><FloppyDiskSolid/>SAVE</Button>