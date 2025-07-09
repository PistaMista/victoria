<script lang="ts">
    import type { ActionInvocation } from "$lib/types/thought";
    import { HammerSolid } from "flowbite-svelte-icons";
    import { entries } from "happy-dom/lib/PropertySymbol.js";
    
    export let content: ActionInvocation;
</script>

<div class="flex flex-col space-y-2">
    <div class="w-full">
        <HammerSolid class="float-left mr-2"/>
        <div class="w-full font-semibold">
            {content.name}
        </div>
        <ul>
            {#each Object.entries(content.parameters) as [name, val]}
                <li>{name}: {val.toString()}</li>
            {/each}
        </ul>
    </div>
</div>