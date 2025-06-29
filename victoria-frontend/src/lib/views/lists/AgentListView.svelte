<script>
    import ListViewHeaderButton from "$lib/components/buttons/ListViewHeaderButton.svelte";
    import AgentCard from "$lib/components/cards/AgentCard.svelte";
    import ListViewHeaderSearchBar from "$lib/components/search/ListViewHeaderSearchBar.svelte";
    import ListView from "$lib/views/ListView.svelte";
    import { PlusOutline } from "flowbite-svelte-icons";
</script>

<ListView cards>
    <ListViewHeaderSearchBar slot="header"/>
    <div slot="header" class="mx-2 content-center flex flex-row">
        <ListViewHeaderButton><PlusOutline class="w-6 h-6"/></ListViewHeaderButton>
    </div>
    
    <AgentCard slot="items"/>
    <AgentCard slot="items"/>
</ListView>