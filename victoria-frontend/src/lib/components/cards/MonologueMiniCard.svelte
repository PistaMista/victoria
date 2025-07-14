<script lang="ts">
    import { ClockOutline, CheckCircleOutline, CloseCircleOutline, ExclamationCircleOutline } from "flowbite-svelte-icons";
    import type { MonologueListItem } from "$lib/types/monologue";
    import { goto } from "$app/navigation";
    
    export let monologue: MonologueListItem;
    
    function goToDetail() {
        goto(`/monologues/${monologue.id}`)
    }
</script>

<button on:click={goToDetail} class="flex bg-slate-400 p-1 rounded-md">
    {monologue.title}
    <div class="grow mx-2"/>
    
    {#if monologue.status === 'PENDING'}
        <ExclamationCircleOutline/>
    {:else if monologue.status === 'RUNNING'}
        <ClockOutline/>
    {:else if monologue.status === 'SUCCESS'}
        <CheckCircleOutline/>
    {:else if monologue.status === 'FAILURE'}
        <CloseCircleOutline/>
    {/if}
</button>