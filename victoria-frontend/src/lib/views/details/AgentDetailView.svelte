<script lang="ts">
    import CreateButton from "$lib/components/buttons/CreateButton.svelte";
import DeleteButton from "$lib/components/buttons/DeleteButton.svelte";
    import SaveButton from "$lib/components/buttons/SaveButton.svelte";
    import GeneralDropdown from "$lib/components/dropdowns/GeneralDropdown.svelte";
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import ParameterSlider from "$lib/components/sliders/ParameterSlider.svelte";
    import ActionToggle from "$lib/components/toggles/ActionToggle.svelte";
    import TriggerToggle from "$lib/components/toggles/TriggerToggle.svelte";
    import DetailView from "$lib/views/DetailView.svelte";
    import { Textarea, Button } from "flowbite-svelte";
</script>


<DetailView title="Researcher">
    <DetailViewSection title="Thumbnail">
        <div class="place-self-center">
            <div class="w-48 h-48 bg-yellow-200 rounded-md"></div>
            <Button class="m-2">Pick image</Button>
        </div>
    </DetailViewSection>
    
    <DetailViewSection title="Base model">
        <!-- Dropdown to select base model -->
        <GeneralDropdown/>
    </DetailViewSection>
    
    <DetailViewSection title="System prompt">
        <Textarea/>
    </DetailViewSection>
    
    <DetailViewSection title="Model parameters">
        <ParameterSlider/>
        <ParameterSlider/>
        <ParameterSlider/>
    </DetailViewSection>
    
    <DetailViewSection title="Triggers">
        <TriggerToggle/>
        <TriggerToggle/>
        <TriggerToggle/>
        <TriggerToggle/>
    </DetailViewSection>
    
    <DetailViewSection title="Actions">
        <ActionToggle/>
        <ActionToggle/>
        <ActionToggle/>
        <ActionToggle/>
    </DetailViewSection>
    
    <DetailViewSection title="Delete agent">
        <DeleteButton/>
    </DetailViewSection>
    
    <DetailViewSection title="Save agent">
        <SaveButton/>
    </DetailViewSection>

    <DetailViewSection title="Create agent">
        <CreateButton/>
    </DetailViewSection>
</DetailView>