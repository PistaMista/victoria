<script>
    import CreateButton from "$lib/components/buttons/CreateButton.svelte";
    import DeleteButton from "$lib/components/buttons/DeleteButton.svelte";
    import SaveButton from "$lib/components/buttons/SaveButton.svelte";
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import DetailView from "$lib/views/DetailView.svelte";
    import { Input } from "flowbite-svelte";
</script>

<DetailView backRoute="/admin/settings/connections">
    <DetailViewSection title="URL">
        <Input/>
    </DetailViewSection>

    <DetailViewSection title="API Key">
        <Input/>
    </DetailViewSection>
    
    <DetailViewSection title="Save connection">
        <SaveButton/>
    </DetailViewSection>
    
    <DetailViewSection title="Delete connection">
        <DeleteButton/>
    </DetailViewSection>
    
    <DetailViewSection title="Create connection">
        <CreateButton/>
    </DetailViewSection>
</DetailView>