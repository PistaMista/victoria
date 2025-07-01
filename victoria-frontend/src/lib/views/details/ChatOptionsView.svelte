<script lang="ts">
    import DeleteButton from "$lib/components/buttons/DeleteButton.svelte";
    import SaveButton from "$lib/components/buttons/SaveButton.svelte";
    import ChatReceiverDropdown from "$lib/components/dropdowns/ChatReceiverDropdown.svelte";
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import ActionToggle from "$lib/components/toggles/ActionToggle.svelte";
    import DetailView from "$lib/views/DetailView.svelte";
</script>

<DetailView>
    <DetailViewSection title="Message recipient">
        <ChatReceiverDropdown/>
    </DetailViewSection>
    
    <DetailViewSection title="Allowed actions">
        <ActionToggle/>
    </DetailViewSection>
    
    <DetailViewSection title="Delete chat">
        <DeleteButton/>
    </DetailViewSection>
    
    <DetailViewSection title="Save chat options">
        <SaveButton/>
    </DetailViewSection>
</DetailView>