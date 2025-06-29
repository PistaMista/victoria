<script>
    import ListViewHeaderButton from "$lib/components/buttons/ListViewHeaderButton.svelte";
    import ActionRepositoryListItem from "$lib/components/lists/items/ActionRepositoryListItem.svelte";
    import ListViewHeaderSearchBar from "$lib/components/search/ListViewHeaderSearchBar.svelte";
    import ListView from "$lib/views/ListView.svelte";
    import { PlusOutline } from "flowbite-svelte-icons";
</script>

<ListView backRoute="/admin">
    <svelte:fragment slot="header">
        <ListViewHeaderSearchBar/>
        <ListViewHeaderButton><PlusOutline class="w-6 h-8 my-auto"/></ListViewHeaderButton>
    </svelte:fragment>

    <svelte:fragment slot="items">
        <ActionRepositoryListItem/>

    </svelte:fragment>
</ListView>