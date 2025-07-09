<script lang="ts">
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
    import type { Trigger } from "$lib/types/trigger";
    import { getDiff } from "$lib/types/diff";
    import { onMount } from "svelte";
    import { createTrigger, deleteTrigger, getTrigger, updateTrigger } from "$lib/api/triggers";
    import type { Option } from "$lib/components/dropdowns/GeneralDropdown.svelte";
    
    export let id: number | null;
    
    let loadedTrigger: Trigger = {
        id: 0,
        name: "",
        settings: {
            type: 'chat',
            receiver: ""
        },
        template: "",
        parser: 'identity'
    };
    let modifiedTrigger: Trigger = structuredClone(loadedTrigger);

    $: changes = getDiff(loadedTrigger, modifiedTrigger);

    let chosenTypeOption: Option | null = null;
    $: modifiedTrigger.settings.type = chosenTypeOption?.value ?? 'chat';

    onMount(async () => {
        if (id !== null) {
            loadedTrigger = await getTrigger(id);
            modifiedTrigger = structuredClone(loadedTrigger);
            chosenTypeOption = {
                displayName: modifiedTrigger.settings.type,
                ariaLabel: modifiedTrigger.settings.type,
                value: modifiedTrigger.settings.type
            }
        }
    });
    
    async function onSave() {
        if (id !== null) {
            await updateTrigger(id, changes);
        }
    }
    
    async function onDelete() {
        if (id !== null) {
            await deleteTrigger(id);
        }
    }
    
    async function onCreate() {
        await createTrigger(modifiedTrigger);
    }
</script>

<DetailView backRoute="/admin/triggers">
    <DetailViewSection title="Trigger">
        <LabeledSetting label="Name">
            <Input bind:value={modifiedTrigger.name} />
        </LabeledSetting>

        <LabeledSetting label="Type">
            <!-- TODO: Make the GeneralDropdown easier to use -->
            <GeneralDropdown
                placeholder="Select type..."
                options={[
                    {displayName: "Chat", ariaLabel: "Chat", value: 'chat'},
                    {displayName: "Timer", ariaLabel: "Timer", value: 'timer'},
                    {displayName: "Poll", ariaLabel: "Poll", value: 'poll'},
                ]}
                bind:chosenOption={chosenTypeOption}
            />
        </LabeledSetting>
        
        {#if modifiedTrigger.settings.type === 'poll'}
            <PollTriggerSettings bind:settings={modifiedTrigger.settings}/>
        {:else if modifiedTrigger.settings.type === 'timer'}
            <TimerTriggerSettings bind:settings={modifiedTrigger.settings}/>
        {:else if modifiedTrigger.settings.type === 'chat'}
            <ChatTriggerSettings bind:settings={modifiedTrigger.settings}/>
        {/if}
    </DetailViewSection>
    
    <DetailViewSection title="Parser">
    </DetailViewSection>
    
    <DetailViewSection title="Template">
        <EventTemplateEditor
            variables={["content"]}
            bind:template={modifiedTrigger.template}
        />
    </DetailViewSection>
    
    {#if id !== null}
        <DetailViewSection title="Delete trigger">
            <DeleteButton
                aria-label="Delete trigger"
                onclick={onDelete}
            />
        </DetailViewSection>
        
        <DetailViewSection title="Save trigger">
            <SaveButton
                aria-label="Save trigger"
                onclick={onSave}
            />
        </DetailViewSection>
    {:else}
        <DetailViewSection title="Create trigger">
            <CreateButton
                aria-label="Create trigger"
                onclick={onCreate}
            />
        </DetailViewSection>
    {/if}
</DetailView>