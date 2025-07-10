<script lang="ts">
    import { getAllActions } from "$lib/api/actions";
    import { getAllTriggers } from "$lib/api/triggers";
    import CreateButton from "$lib/components/buttons/CreateButton.svelte";
    import DeleteButton from "$lib/components/buttons/DeleteButton.svelte";
    import SaveButton from "$lib/components/buttons/SaveButton.svelte";
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import { getDiff } from "$lib/types/diff";
    import type { TriggerListItem } from "$lib/types/trigger";
    import type { Action } from "$lib/types/action";
    import type { User } from "$lib/types/user";
    import DetailView from "$lib/views/DetailView.svelte";
    import { Checkbox, Input } from "flowbite-svelte";
    import { createUser, deleteUser, getUser, updateUser } from "$lib/api/users";
    import { onMount } from "svelte";
    import Toggle from "$lib/components/toggles/Toggle.svelte";
    import Loader from "$lib/components/placeholders/Loader.svelte";
    
    export let id: number | null;
    
    let loadedUser: User = {
        id: 0,
        username: "",
        newPassword: "",
        role: "user",
        permittedActions: [],
        permittedTriggers: []
    }
    let modifiedUser: User = structuredClone(loadedUser);
    $: changes = getDiff(loadedUser, modifiedUser);
    
    let adminRoleChecked: boolean = modifiedUser.role === 'admin';
    $: modifiedUser.role = adminRoleChecked ? 'admin' : 'user';

    let actions: [Action, boolean][] = [];
    let triggers: [TriggerListItem, boolean][] = [];

    $: modifiedUser.permittedActions = actions.filter(([_, e]) => e).map(([v, _]) => v.id);
    $: modifiedUser.permittedTriggers = triggers.filter(([_, e]) => e).map(([v, _]) => v.id);
    
    let dataPromise: Promise<any> = Promise.resolve();
    let deletePromise: Promise<any> = Promise.resolve();
    let savePromise: Promise<any> = Promise.resolve();
    let createPromise: Promise<any> = Promise.resolve();

    async function load() {
        if (id !== null) {
            loadedUser = await getUser(id);
            modifiedUser = structuredClone(loadedUser);
        }
        actions = (await getAllActions()).map(
            (val) => [val, loadedUser.permittedActions.includes(val.id)]
        )
        triggers = (await getAllTriggers()).map(
            (val) => [val, loadedUser.permittedTriggers.includes(val.id)]
        )
    }

    async function onDelete() {
        deletePromise = deleteUser(loadedUser.id);
    }
    
    async function onSave() {
        savePromise = updateUser(modifiedUser.id, changes);
    }
    
    async function onCreate() {
        createPromise = createUser(modifiedUser);
    }
    
    onMount(async () => {
        dataPromise = load();
    })
</script>

<Loader
    promise={dataPromise}
    pendingMessage="Loading user details..."
    rejectMessage="Failed to load user"
>
<Loader
    promise={deletePromise}
    pendingMessage="Deleting user..."
    rejectMessage="Failed to delete user"
>
<Loader
    promise={savePromise}
    pendingMessage="Saving changes..."
    rejectMessage="Failed to save changes"
>
<Loader
    promise={createPromise}
    pendingMessage="Creating user..."
    rejectMessage="Failed to create user"
>
<DetailView backRoute="/admin/users">
    <DetailViewSection title="Username">
        <Input 
            aria-label="Username"
            bind:value={modifiedUser.username}
        />
    </DetailViewSection>
    
    <DetailViewSection title="New password">
        <Input 
            aria-label="New password"
            bind:value={modifiedUser.newPassword}
        />
    </DetailViewSection>
    
    <DetailViewSection title="Enable admin role">
        <Checkbox
            aria-label="Enable admin role"
            bind:checked={adminRoleChecked}
        />
    </DetailViewSection>

    <DetailViewSection title="Permitted agent triggers">
        <div class="flex flex-col space-y-2">
            {#each triggers as trigger}
                <Toggle
                    label={trigger[0].name}
                    aria-label={trigger[0].name}
                    bind:enabled={trigger[1]}
                />
            {/each}
        </div>
    </DetailViewSection>
    
    <DetailViewSection title="Permitted agent actions">
        <div class="flex flex-col space-y-2">
            {#each actions as action}
                <Toggle
                    label={action[0].displayName}
                    aria-label={action[0].displayName}
                    bind:enabled={action[1]}
                />
            {/each}
        </div>
    </DetailViewSection>
    
    <DetailViewSection title="Delete user">
        <DeleteButton
            aria-label="Delete user"
            onclick={onDelete}
        />
    </DetailViewSection>

    <DetailViewSection title="Save user">
        <SaveButton
            aria-label="Save user"
            onclick={onSave}
        />
    </DetailViewSection>

    <DetailViewSection title="Create user">
        <CreateButton
            aria-label="Create user"
            onclick={onCreate}
        />
    </DetailViewSection>
</DetailView>
</Loader>
</Loader>
</Loader>
</Loader>