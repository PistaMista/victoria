<script>
    import OptionsRouteButton from "$lib/components/buttons/OptionsRouteButton.svelte";
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import DetailView from "$lib/views/DetailView.svelte";
    import { LinkOutline, CogSolid, BrainSolid } from "flowbite-svelte-icons";
</script>

<DetailView backRoute="/admin">
    <DetailViewSection title="Settings">
        <OptionsRouteButton icon={CogSolid} text="General"/>        
        <OptionsRouteButton icon={LinkOutline} text="Connections"/>
        <OptionsRouteButton icon={BrainSolid} text="Models"/>
    </DetailViewSection>
</DetailView>