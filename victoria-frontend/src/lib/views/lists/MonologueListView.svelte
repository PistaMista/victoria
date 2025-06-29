<script lang="ts">
    import ListView from "../ListView.svelte";
    import ListViewHeaderSearchBar from "$lib/components/search/ListViewHeaderSearchBar.svelte";
    import ListViewHeaderDropdown from "$lib/components/dropdowns/ListViewHeaderDropdown.svelte";
    import MonologueListItem from "$lib/components/lists/items/MonologueListItem.svelte";
</script>

<ListView>
    <ListViewHeaderSearchBar slot="header"/>
    <div slot="header" class="mx-2 content-center flex flex-row">
        <!-- Filter by trigger type -->
        <ListViewHeaderDropdown/>
        <!-- Filter by monologue status -->
        <ListViewHeaderDropdown/>
        <!-- Filter by assigned agent -->
        <ListViewHeaderDropdown/>
    </div>


    <MonologueListItem slot="items"/>
    <MonologueListItem slot="items"/>
</ListView>