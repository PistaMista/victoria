<script>
    import ListViewHeaderButton from "$lib/components/buttons/ListViewHeaderButton.svelte";
    import TriggerListItem from "$lib/components/lists/items/TriggerListItem.svelte";
    import ListViewHeaderSearchBar from "$lib/components/search/ListViewHeaderSearchBar.svelte";
    import ListView from "$lib/views/ListView.svelte";
    import { PlusOutline } from "flowbite-svelte-icons";
</script>

<ListView backRoute="/admin">
    <ListViewHeaderSearchBar slot="header"/>
    <ListViewHeaderButton slot="header"><PlusOutline class="w-6 h-8 my-auto"/></ListViewHeaderButton>
    
    <TriggerListItem slot="items"/>
    <TriggerListItem slot="items"/>
    <TriggerListItem slot="items"/>
</ListView>