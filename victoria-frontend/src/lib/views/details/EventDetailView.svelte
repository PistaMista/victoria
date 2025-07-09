<script lang="ts">
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import DetailView from "$lib/views/DetailView.svelte";
    import { onMount } from "svelte";
    import type { Event } from "$lib/types/event";
    import { getEvent } from "$lib/api/events";
    import { getTrigger } from "$lib/api/triggers";

    export let id: number;
    
    let loadedEvent: Event = {
        triggerId: 0,
        content: "None"
    };
    let triggerName: string = "";


    onMount(async () => {
        loadedEvent = await getEvent(id);
        triggerName = (await getTrigger(loadedEvent.triggerId)).name;
    })
</script>

<DetailView>
    <DetailViewSection title="Trigger">
        {triggerName}
    </DetailViewSection>
    
    <DetailViewSection title="Content">
        {loadedEvent.content}
    </DetailViewSection>
</DetailView>