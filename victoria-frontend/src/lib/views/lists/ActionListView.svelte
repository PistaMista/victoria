<script lang="ts">
    import { getActionRepositories } from "$lib/api/action_repositories";
    import ListViewHeaderButton from "$lib/components/buttons/ListViewHeaderButton.svelte";
    import ActionRepositoryListItem from "$lib/components/lists/items/ActionRepositoryListItem.svelte";
    import ListViewHeaderSearchBar from "$lib/components/search/ListViewHeaderSearchBar.svelte";
    import type { ActionRepository } from "$lib/types/action_repo";
    import ListView from "$lib/views/ListView.svelte";
    import { PlusOutline } from "flowbite-svelte-icons";
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    
    let repositories: ActionRepository[] = [];
    let searchQuery: string = "";
    let mounted = false;
    
    function createActionRepository() {
        goto("/admin/actions/add");
    }
    
    onMount(() => {
        mounted = true;
    })
    
    $: if (mounted) {
        (async () => {
            let query: string | null = searchQuery ? searchQuery : null;
            repositories = await getActionRepositories(query);
        })();
    }
</script>

<ListView backRoute="/admin">
    <svelte:fragment slot="header">
        <ListViewHeaderSearchBar
            ontype={(val) => searchQuery = val}
        />
        <ListViewHeaderButton
            onclick={createActionRepository}
            aria-label="Create action repository"
        ><PlusOutline class="w-6 h-8 my-auto"/></ListViewHeaderButton>
    </svelte:fragment>

    <svelte:fragment slot="items">
        {#each repositories as repo}
            <ActionRepositoryListItem
                repository={repo}
            />
        {/each}
    </svelte:fragment>
</ListView>