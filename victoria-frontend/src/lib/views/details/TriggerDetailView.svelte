<script>
    import CreateButton from "$lib/components/buttons/CreateButton.svelte";
    import DeleteButton from "$lib/components/buttons/DeleteButton.svelte";
    import SaveButton from "$lib/components/buttons/SaveButton.svelte";
    import GeneralDropdown from "$lib/components/dropdowns/GeneralDropdown.svelte";
    import EventTemplateEditor from "$lib/components/editors/EventTemplateEditor.svelte";
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import LabeledSetting from "$lib/components/sections/LabeledSetting.svelte";
    import ChatTriggerSettings from "$lib/components/triggers/ChatTriggerSettings.svelte";
    import PollTriggerSettings from "$lib/components/triggers/PollTriggerSettings.svelte";
    import TimerTriggerSettings from "$lib/components/triggers/TimerTriggerSettings.svelte";
    import DetailView from "$lib/views/DetailView.svelte";
    import { Input } from "flowbite-svelte";
</script>

<DetailView backRoute="/admin/triggers">
    <DetailViewSection title="Trigger">
        <LabeledSetting label="Name">
            <Input/>
        </LabeledSetting>

        <LabeledSetting label="Type">
            <!-- Type: TIMER, CHAT, WEBHOOK, POLL-->
            <GeneralDropdown/>
        </LabeledSetting>
        
        <PollTriggerSettings/>
        <ChatTriggerSettings/>
        <TimerTriggerSettings/>
    </DetailViewSection>
    
    <DetailViewSection title="Parser">
        <LabeledSetting label="Type">
            <GeneralDropdown/>
        </LabeledSetting>

        <LabeledSetting label="Settings">
            SOME SETTINGS TO CHANGE
        </LabeledSetting>
    </DetailViewSection>
    
    <DetailViewSection title="Template">
        <EventTemplateEditor/>
    </DetailViewSection>
    
    <DetailViewSection title="Delete trigger">
        <DeleteButton/>
    </DetailViewSection>
    
    <DetailViewSection title="Save trigger">
        <SaveButton/>
    </DetailViewSection>
    
    <DetailViewSection title="Create trigger">
        <CreateButton/>
    </DetailViewSection>
</DetailView>