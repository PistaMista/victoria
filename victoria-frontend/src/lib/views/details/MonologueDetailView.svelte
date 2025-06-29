<script>
    import DetailView from "../DetailView.svelte";
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import MonologueStatusIndicator from "$lib/components/indicators/MonologueStatusIndicator.svelte";
    import AgentCard from "$lib/components/cards/AgentCard.svelte";
    import ThoughtTimeline from "$lib/components/monologue/ThoughtTimeline.svelte";
    import AbortButton from "$lib/components/buttons/AbortButton.svelte";
</script>

<DetailView>
    <DetailViewSection title="Summary">
        <div class="border-b-2 font-semibold">
            Research thesis ideas
        </div>
        <div>
            Searching for sources on the web
        </div>
    </DetailViewSection>

    <DetailViewSection title="Status">
        <MonologueStatusIndicator/>
    </DetailViewSection>

    <DetailViewSection title="Assigned agent">
        <AgentCard/>
    </DetailViewSection>

    <DetailViewSection title="Thoughts">
        <ThoughtTimeline/>
    </DetailViewSection>
    
    <DetailViewSection title="Abort monologue">
        <AbortButton/>
    </DetailViewSection>
</DetailView>