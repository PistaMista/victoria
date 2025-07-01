<script lang="ts">
    import ListViewHeaderButton from "$lib/components/buttons/ListViewHeaderButton.svelte";
    import ListViewHeaderDropdown from "$lib/components/dropdowns/ListViewHeaderDropdown.svelte";
    import ChatListItem from "$lib/components/lists/items/ChatListItem.svelte";
    import ListViewHeaderSearchBar from "$lib/components/search/ListViewHeaderSearchBar.svelte";
    import ListView from "$lib/views/ListView.svelte";
    import { PlusOutline } from "flowbite-svelte-icons";
</script>

<ListView>
    <svelte:fragment slot="header">
        <ListViewHeaderSearchBar/>
        <div class="mx-2 content-center flex flex-row">
            <!-- Sort by Recent/Longest/Important -->
            <ListViewHeaderDropdown/>
            <!-- Filter by chat receiver -->
            <ListViewHeaderDropdown/>

            <ListViewHeaderButton><PlusOutline class="w-6 h-6"/></ListViewHeaderButton>
        </div>
    </svelte:fragment>

    
    <svelte:fragment slot="items">
        <ChatListItem/>
        <ChatListItem/>
        <ChatListItem/>
    </svelte:fragment>
</ListView>