<script>
    import CreateButton from "$lib/components/buttons/CreateButton.svelte";
    import DeleteButton from "$lib/components/buttons/DeleteButton.svelte";
    import SaveButton from "$lib/components/buttons/SaveButton.svelte";
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import ActionToggle from "$lib/components/toggles/ActionToggle.svelte";
    import TriggerToggle from "$lib/components/toggles/TriggerToggle.svelte";
    import DetailView from "$lib/views/DetailView.svelte";
    import { Checkbox, Input } from "flowbite-svelte";
</script>

<DetailView backRoute="/admin/users">
    <DetailViewSection title="Username">
        <Input/>
    </DetailViewSection>
    
    <DetailViewSection title="New password">
        <Input/>
    </DetailViewSection>
    
    <DetailViewSection title="Enable admin role">
        <Checkbox/>
    </DetailViewSection>

    <DetailViewSection title="Permitted agent triggers">
        <div class="flex flex-col space-y-2">
            <TriggerToggle/>
            <TriggerToggle/>
            <TriggerToggle/>
        </div>
    </DetailViewSection>
    
    <DetailViewSection title="Permitted agent actions">
        <div class="flex flex-col space-y-2">
            <ActionToggle/>
            <ActionToggle/>
            <ActionToggle/>
        </div>
    </DetailViewSection>
    
    <DetailViewSection title="Delete user">
        <DeleteButton/>
    </DetailViewSection>

    <DetailViewSection title="Save user">
        <SaveButton/>
    </DetailViewSection>

    <DetailViewSection title="Create user">
        <CreateButton/>
    </DetailViewSection>
</DetailView>