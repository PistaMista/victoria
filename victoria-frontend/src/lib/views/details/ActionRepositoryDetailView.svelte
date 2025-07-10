<script lang="ts">
    import CreateButton from "$lib/components/buttons/CreateButton.svelte";
    import DeleteButton from "$lib/components/buttons/DeleteButton.svelte";
    import SaveButton from "$lib/components/buttons/SaveButton.svelte";
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import LabeledSetting from "$lib/components/sections/LabeledSetting.svelte";
    import Loader from "$lib/components/placeholders/Loader.svelte";
    import DetailView from "$lib/views/DetailView.svelte";
    import {  Input } from "flowbite-svelte";
    import type { ActionRepository } from "$lib/types/action_repo";
    import { getDiff, type Diff } from "$lib/types/diff";
    import { onMount } from "svelte";
    import { createActionRepository, deleteActionRepository, getActionRepository, updateActionRepository } from "$lib/api/action_repositories";
    
    export let id: number | null;
    let loadedRepo: ActionRepository = {
        id: 0,
        name: "",
        url: ""
    };
    let modifiedRepo: ActionRepository = loadedRepo;
    $: changes = getDiff(loadedRepo, modifiedRepo);
    
    let dataPromise: Promise<any> = Promise.resolve();
    let deletePromise: Promise<any> = Promise.resolve();
    let savePromise: Promise<any> = Promise.resolve();
    let createPromise: Promise<any> = Promise.resolve();
    
    onMount(() => {
        dataPromise = (async () => {
            if (id !== null) {
                loadedRepo = await getActionRepository(id);
                modifiedRepo = structuredClone(loadedRepo);
            }
        })();
    });
    
    function deleteRepo() {
        deletePromise = deleteActionRepository(loadedRepo.id);
    }
    
    function saveRepo() {
        savePromise = updateActionRepository(loadedRepo.id, changes);
    }
    
    function createRepo() {
        createPromise = createActionRepository(modifiedRepo);
    }
</script>

<Loader
    promise={dataPromise}
    pendingMessage="Loading action repository details..."
    rejectMessage="Failed to load action repository"
>
<Loader
    promise={deletePromise}
    pendingMessage="Deleting action repository..."
    rejectMessage="Failed to delete action repository"
>
<Loader
    promise={savePromise}
    pendingMessage="Saving changes..."
    rejectMessage="Failed to save changes"
>
<Loader
    promise={createPromise}
    pendingMessage="Creating action repository..."
    rejectMessage="Failed to create action repository"
>
<DetailView backRoute="/admin/actions">
    <DetailViewSection title="Action repository">
        <div class="flex flex-col space-y-2">
            <LabeledSetting label="Name">
                <Input bind:value={modifiedRepo.name}/>
            </LabeledSetting>
            <LabeledSetting label="URL">
                <Input bind:value={modifiedRepo.url}/>
            </LabeledSetting>
        </div>
    </DetailViewSection>
    
    {#if id === null}
        <DetailViewSection title="Create action repository">
            <CreateButton aria-label="Create action repository" onclick={createRepo}/>
        </DetailViewSection>
    {:else}
        <DetailViewSection title="Delete action repository">
            <DeleteButton aria-label="Delete action repository" onclick={deleteRepo}/>
        </DetailViewSection>

        <DetailViewSection title="Save action repository">
            <SaveButton aria-label="Save action repository" onclick={saveRepo}/>
        </DetailViewSection>
    {/if}
</DetailView>
</Loader>
</Loader>
</Loader>
</Loader>
