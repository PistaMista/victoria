<script lang="ts">
    import ListView from "../ListView.svelte";
    import ListViewHeaderSearchBar from "$lib/components/search/ListViewHeaderSearchBar.svelte";
    import ListViewHeaderDropdown from "$lib/components/dropdowns/ListViewHeaderDropdown.svelte";
    import MonologueListItem from "$lib/components/lists/items/MonologueListItem.svelte";
</script>

<ListView>

    <svelte:fragment slot="header">
        <ListViewHeaderSearchBar/>
        <div class="mx-2 content-center flex flex-row">
            <!-- Filter by trigger type -->
            <ListViewHeaderDropdown/>
            <!-- Filter by monologue status -->
            <ListViewHeaderDropdown/>
            <!-- Filter by assigned agent -->
            <ListViewHeaderDropdown/>
        </div>
    </svelte:fragment>

    <svelte:fragment slot="items">
        <MonologueListItem/>
        <MonologueListItem/>
    </svelte:fragment>
</ListView>