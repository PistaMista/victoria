<script>
    import CreateButton from "$lib/components/buttons/CreateButton.svelte";
    import SaveButton from "$lib/components/buttons/SaveButton.svelte";
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import LabeledSetting from "$lib/components/sections/LabeledSetting.svelte";
    import DetailView from "$lib/views/DetailView.svelte";
    import {  Input } from "flowbite-svelte";
</script>

<DetailView backRoute="/admin/actions">
    <DetailViewSection title="Action repository">
        <div class="flex flex-col space-y-2">
            <LabeledSetting label="Name">
                <Input/>
            </LabeledSetting>
            <LabeledSetting label="URL">
                <Input/>
            </LabeledSetting>
        </div>
    </DetailViewSection>
    
    <DetailViewSection title="Save action repository">
        <SaveButton/>
    </DetailViewSection>
    
    <DetailViewSection title="Create action repository">
        <CreateButton/>
    </DetailViewSection>
</DetailView>