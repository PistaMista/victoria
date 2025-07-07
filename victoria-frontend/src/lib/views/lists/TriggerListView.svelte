<script lang="ts">
    import ListViewHeaderButton from "$lib/components/buttons/ListViewHeaderButton.svelte";
    import ItemComponent from "$lib/components/lists/items/TriggerListItem.svelte";
    import ListViewHeaderSearchBar from "$lib/components/search/ListViewHeaderSearchBar.svelte";
    import ListView from "$lib/views/ListView.svelte";
    import { PlusOutline } from "flowbite-svelte-icons";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import type { TriggerListItem } from "$lib/types/trigger";
    import { getAllTriggers } from "$lib/api/triggers";

    let triggers: TriggerListItem[] = [];
    let searchQuery: string = "";
    let mounted: Boolean = false;

    function createTrigger() {
        goto("/admin/triggers/add");
    }

    onMount(() => {
        mounted = true;
    })
    
    $: if (mounted) {
        (async () => {
            let query = searchQuery ? searchQuery : null;
            triggers = await getAllTriggers(query);        
        })();
    }
</script>

<ListView backRoute="/admin">
    <svelte:fragment slot="header">
        <ListViewHeaderSearchBar
            ontype={(val) => searchQuery = val}
        />
        <ListViewHeaderButton
            onclick={createTrigger}
            aria-label="Create trigger"
        ><PlusOutline class="w-6 h-8 my-auto"/></ListViewHeaderButton>
    </svelte:fragment>
    
    <svelte:fragment slot="items">
        {#each triggers as trigger}
            <ItemComponent 
                {trigger}
            />
        {/each}
    </svelte:fragment>
</ListView>