<script lang="ts">
    import DetailView from "../DetailView.svelte";
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import MonologueStatusIndicator from "$lib/components/indicators/MonologueStatusIndicator.svelte";
    import AgentCard from "$lib/components/cards/AgentCard.svelte";
    import ThoughtTimeline from "$lib/components/monologue/ThoughtTimeline.svelte";
    import AbortButton from "$lib/components/buttons/AbortButton.svelte";
    import type { Monologue } from "$lib/types/monologue";
    import type { Agent } from "$lib/types/agent";
    import { abortMonologue, getMonologue } from "$lib/api/monologues";
    import { onMount } from "svelte";

    export let id: number;
    
    let monologue: Monologue = {
        id: 0,
        agentId: 0,
        startTimestamp: 0,
        endTimestamp: 0,
        title: "",
        summary: "",
        status: "PENDING"
    };

    let agent: Agent | null = null;
    
    async function onAbort() {
        await abortMonologue(id);
    }
    
    onMount(async () => {
        monologue = await getMonologue(id);
    })
</script>

<DetailView>
    <DetailViewSection title="Summary">
        <div class="border-b-2 font-semibold">
            {monologue.title}
        </div>
        <div>
            {monologue.summary}
        </div>
    </DetailViewSection>

    <DetailViewSection title="Status">
        <MonologueStatusIndicator
            horizontal
            status={monologue.status}
            startTimestamp={monologue.startTimestamp}
            endTimestamp={monologue.endTimestamp}

            displayRuntime
            displayStartDate
            displayEndDate
        />
    </DetailViewSection>

    <DetailViewSection title="Assigned agent">
        {#if agent}
            <AgentCard {agent}/>
        {/if}
    </DetailViewSection>

    <DetailViewSection title="Thoughts">
        <ThoughtTimeline monologueId={id}/>
    </DetailViewSection>
    
    <DetailViewSection title="Abort monologue">
        <AbortButton aria-label="Abort monologue" onclick={onAbort}/>
    </DetailViewSection>
</DetailView>