<script lang="ts">
    import type { Thought } from "$lib/types/thought";
    import { onMount } from "svelte";
    import ItemComponent from "./Thought.svelte";
    import { getMonologueThoughts } from "$lib/api/monologues";
    
    export let monologueId: number;
    
    let thoughts: Thought[] = [];

    onMount(async () => {
        thoughts = await getMonologueThoughts(monologueId);
    })
</script>

<div class="relative flex flex-col px-2 py-2 space-y-12">
    {#each thoughts as thought}
        <ItemComponent {thought}/>
    {/each}

    <!-- Dotted line for decoration-->
    <div class="absolute z-10 top-0 bottom-4 left-6 w-0.5 border-l-4 border-dotted border-gray-200"/>
</div>