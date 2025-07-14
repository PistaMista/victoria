<script lang="ts">
    import { getPermittedActions } from "$lib/api/actions";
    import { deleteChat, getChatOptions, getChatReceivers, updateChatOptions } from "$lib/api/chatting";
    import DeleteButton from "$lib/components/buttons/DeleteButton.svelte";
    import SaveButton from "$lib/components/buttons/SaveButton.svelte";
    import ChatReceiverDropdown from "$lib/components/dropdowns/ChatReceiverDropdown.svelte";
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import Toggle from "$lib/components/toggles/Toggle.svelte";
    import Loader from "$lib/components/placeholders/Loader.svelte";
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
    
    let initPromise: Promise<any> = Promise.resolve();
    let dataPromise: Promise<any> = Promise.resolve();
    let savePromise: Promise<any> = Promise.resolve();
    let deletePromise: Promise<any> = Promise.resolve();
    
    async function init() {
        actions = (await getPermittedActions()).map(
            (val) => [val, loadedOptions.enabledActionIds.includes(val.id)]
        )
    }
    
    async function load() {
        loadedOptions = await getChatOptions(id);
        modifiedOptions = structuredClone(loadedOptions);
    }
    
    function onSave() {
        savePromise = updateChatOptions(id, changes);
    }
    
    function onDelete() {
        deletePromise = deleteChat(id);
    }

    onMount(async () => {
        initPromise = init();
        dataPromise = load();
    })
</script>

<Loader
    promise={initPromise}
    pendingMessage="Initializing view..."
    rejectMessage="Failed to initialize view"
>
<Loader
    promise={dataPromise}
    pendingMessage="Loading chat options..."
    rejectMessage="Failed to load chat options"
>
<Loader
    promise={savePromise}
    pendingMessage="Saving chat options"
    rejectMessage="Failed to save chat options"
>
<Loader
    promise={deletePromise}
    pendingMessage="Deleting chat..."
    rejectMessage="Failed to delete chat"
>
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
</Loader>
</Loader>
</Loader>
</Loader>