<script lang="ts">
    import AgentStatusIndicator from "../indicators/AgentStatusIndicator.svelte";
    import MonologueMiniCard from "./MonologueMiniCard.svelte";
    import { DotsVerticalOutline } from "flowbite-svelte-icons";
    import type { AgentListItem } from "$lib/types/agent";
    import { onMount } from "svelte";
    import { getAgentMonologues } from "$lib/api/agents";
    import type { MonologueListItem } from "$lib/types/monologue";
    import { goto } from "$app/navigation";
    
    export let agent: AgentListItem;
    let monologues: MonologueListItem[] = [];
    let mounted = false;
    
    function goToDetail() {
        goto(`/agents/${agent.id}`);
    }
    
    onMount(() => {
        mounted = true;
    })
    
    $: if (mounted) {
        (async () => {
            monologues = await getAgentMonologues(agent.id);
        })();
    }
</script>

<div class="bg-slate-300 rounded-md p-2 flex flex-col md:w-72 m-1">
    <div class="flex flex-row content-center pl-1 mb-1">
        <div class="font-bold">
            {agent.name}
        </div>
        <div class="grow"/>
        <AgentStatusIndicator status={agent.status}/>
        <button 
            class="hover:bg-slate-500 rounded-md"
            aria-label="{agent.name} agent detail"
            on:click={goToDetail}
        >
            <DotsVerticalOutline/>
        </button>
    </div>
    <div class="flex flex-row">
        <div class="bg-orange-200 rounded-md h-14 w-14 p-1"></div>
        <div class="grow h-24 bg-slate-400 rounded-md ml-1 p-1 overflow-y-scroll">
            <div class="flex flex-col">
                {#each monologues as monologue}
                    <MonologueMiniCard
                        {monologue}
                    />
                {/each}
            </div>
        </div>
    </div>
</div>