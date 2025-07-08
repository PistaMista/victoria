<script lang="ts">
    import CreateButton from "$lib/components/buttons/CreateButton.svelte";
    import DeleteButton from "$lib/components/buttons/DeleteButton.svelte";
    import SaveButton from "$lib/components/buttons/SaveButton.svelte";
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import LabeledSetting from "$lib/components/sections/LabeledSetting.svelte";
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
    
    onMount(async () => {
        if (id !== null) {
            loadedRepo = await getActionRepository(id);
            modifiedRepo = structuredClone(loadedRepo);
        }
    });
    
    async function deleteRepo() {
        await deleteActionRepository(loadedRepo.id);
    }
    
    async function saveRepo() {
        await updateActionRepository(loadedRepo.id, changes);
    }
    
    async function createRepo() {
        await createActionRepository(modifiedRepo);
    }
</script>

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