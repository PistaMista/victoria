<script>
    import ListViewHeaderButton from "$lib/components/buttons/ListViewHeaderButton.svelte";
    import AgentCard from "$lib/components/cards/AgentCard.svelte";
    import ListViewHeaderSearchBar from "$lib/components/search/ListViewHeaderSearchBar.svelte";
    import ListView from "$lib/views/ListView.svelte";
    import { PlusOutline } from "flowbite-svelte-icons";
</script>

<ListView cards>
    
    <svelte:fragment slot="header">
        <ListViewHeaderSearchBar/>
        <div class="mx-2 content-center flex flex-row">
            <ListViewHeaderButton><PlusOutline class="w-6 h-6"/></ListViewHeaderButton>
        </div>
    </svelte:fragment>
    
    <svelte:fragment slot="items">
        <AgentCard/>
        <AgentCard/>
    </svelte:fragment>
</ListView>