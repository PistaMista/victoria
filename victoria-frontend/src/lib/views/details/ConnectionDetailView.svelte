<script lang="ts">
    import { createConnection, deleteConnection, getConnection, updateConnection } from "$lib/api/connection";
    import CreateButton from "$lib/components/buttons/CreateButton.svelte";
    import DeleteButton from "$lib/components/buttons/DeleteButton.svelte";
    import SaveButton from "$lib/components/buttons/SaveButton.svelte";
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import Loader from "$lib/components/placeholders/Loader.svelte";
    import type { Connection } from "$lib/types/connection";
    import { getDiff } from "$lib/types/diff";
    import DetailView from "$lib/views/DetailView.svelte";
    import { Input } from "flowbite-svelte";
    import { onMount } from "svelte";

    export let id: number | null;
    
    // TODO: Create some sort of Modifiable<T> to encapsulate this loaded/modified pattern?
    let loadedConnection: Connection = {
        id: 0,
        name: "",
        url: ""
    };
    let modifiedConnection: Connection = structuredClone(loadedConnection);
    $: changes = getDiff(loadedConnection, modifiedConnection);

    let dataPromise: Promise<any> = Promise.resolve();
    let savePromise: Promise<any> = Promise.resolve();
    let deletePromise: Promise<any> = Promise.resolve();
    let createPromise: Promise<any> = Promise.resolve();

    async function load() {
        if (id !== null) {
            loadedConnection = await getConnection(id);
            modifiedConnection = structuredClone(loadedConnection);
        }
    }

    async function onSave() {
        savePromise = updateConnection(loadedConnection.id, changes);
    }
    
    async function onDelete() {
        deletePromise = deleteConnection(loadedConnection.id);        
    }
    
    async function onCreate() {
        createPromise = createConnection(modifiedConnection);
    }
    
    onMount(() => {
        dataPromise = load();
    })
</script>

<Loader
    promise={dataPromise}
    pendingMessage="Loading connection details..."
    rejectMessage="Failed to load connection details"
>
<Loader
    promise={savePromise}
    pendingMessage="Saving changes..."
    rejectMessage="Failed to save changes"
>
<Loader
    promise={deletePromise}
    pendingMessage="Deleting connection..."
    rejectMessage="Failed to delete connection"
>
<Loader
    promise={createPromise}
    pendingMessage="Creating connection..."
    rejectMessage="Failed to create connection"
>
<DetailView backRoute="/admin/settings/connections">
    <DetailViewSection title="Name">
        <Input
            aria-label="Name"
            bind:value={modifiedConnection.name}
        />
    </DetailViewSection>

    <DetailViewSection title="URL">
        <Input
            aria-label="URL"
            bind:value={modifiedConnection.url}
        />
    </DetailViewSection>

    <DetailViewSection title="Delete connection">
        <DeleteButton
            aria-label="Delete connection"
            onclick={onDelete}
        />
    </DetailViewSection>
    
    <DetailViewSection title="Save connection">
        <SaveButton
            aria-label="Save connection"
            onclick={onSave}
        />
    </DetailViewSection>
    
    
    <DetailViewSection title="Create connection">
        <CreateButton
            aria-label="Create connection"
            onclick={onCreate}
        />
    </DetailViewSection>
</DetailView>
</Loader>
</Loader>
</Loader>
</Loader>