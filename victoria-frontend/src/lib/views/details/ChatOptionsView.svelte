<script lang="ts">
    import { getPermittedActions } from "$lib/api/actions";
    import { deleteChat, getChatOptions, getChatReceivers, updateChatOptions } from "$lib/api/chatting";
    import DeleteButton from "$lib/components/buttons/DeleteButton.svelte";
    import SaveButton from "$lib/components/buttons/SaveButton.svelte";
    import ChatReceiverDropdown from "$lib/components/dropdowns/ChatReceiverDropdown.svelte";
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import Toggle from "$lib/components/toggles/Toggle.svelte";
    import type { Action } from "$lib/types/action";
    import type { ChatOptions } from "$lib/types/chat";
    import { getDiff } from "$lib/types/diff";
    import DetailView from "$lib/views/DetailView.svelte";
    import { onMount } from "svelte";

    export let id: number;
    
    let loadedOptions: ChatOptions = {
        receiver: '',
        enabledActionIds: []
    };
    let modifiedOptions: ChatOptions = structuredClone(loadedOptions);
    $: changes = getDiff(loadedOptions, modifiedOptions);
    
    let actions: [Action, boolean][] = [];
    $: modifiedOptions.enabledActionIds = actions.filter(([_, e]) => e).map(([v, _]) => v.id);
    
    async function initActionToggles() {
        actions = (await getPermittedActions()).map(
            (val) => [val, loadedOptions.enabledActionIds.includes(val.id)]
        )
    }
    
    async function onSave() {
        await updateChatOptions(id, changes);
    }
    
    async function onDelete() {
        await deleteChat(id);
    }

    onMount(async () => {
        loadedOptions = await getChatOptions(id);
        modifiedOptions = structuredClone(loadedOptions);
        await initActionToggles();
    })
</script>

<DetailView>
    <DetailViewSection title="Message recipient">
        <ChatReceiverDropdown
            aria-label="Select chat receiver"
            bind:chosenReceiver={modifiedOptions.receiver}
        />
    </DetailViewSection>
    
    <DetailViewSection title="Allowed actions">
        {#each actions as action}
            <Toggle
                label={action[0].displayName}
                aria-label={action[0].displayName}
                bind:enabled={action[1]}
            />
        {/each}
    </DetailViewSection>
    
    <DetailViewSection title="Delete chat">
        <DeleteButton
            aria-label="Delete chat"
            onclick={onDelete}
        />
    </DetailViewSection>
    
    <DetailViewSection title="Save chat options">
        <SaveButton
            aria-label="Save chat options"
            onclick={onSave}
        />
    </DetailViewSection>
</DetailView>