<script lang="ts">
    import { ButtonGroup, Button } from "flowbite-svelte";
    import type { ComponentType } from "svelte";
    type ContextAction = {
        icon_component: ComponentType,
        action: () => void
    }
    
    export let context_actions: Array<ContextAction> = [];
</script>

<ButtonGroup class="-mt-2 bg-slate-500 text-slate-200">
    {#each context_actions as action}
        <Button on:click={action.action}> <svelte:component this={action.icon_component}/> </Button>
    {/each}
</ButtonGroup>