<script>
    import Button from "$lib/components/button/Button.svelte";
    import { Search } from "flowbite-svelte";   
    import { ChevronLeftOutline, PlusOutline } from "flowbite-svelte-icons";
</script>

<!-- COMPONENT: ActionListView -->
<!-- COMPONENT: ListView -->
<div class="flex flex-col w-full h-full">
    <div class="p-1 bg-slate-400 flex flex-row">
        <!-- COMPONENT: BackButton -->
        <div class="flex flex-row hover:bg-slate-500 rounded-md p-1">
            <ChevronLeftOutline class="h-8 w-8 my-auto"/>
            <div class="content-center mr-2">
                Back
            </div>
        </div>
        <!-- COMPONENT: ListViewHeaderSearchBar -->
        <Search class="grow max-h-10 mb-1 md:mb-0"></Search>
        
        <!-- COMPONENT: ListViewHeaderButton -->
        <div class="hover:bg-slate-300 p-1 rounded-md">
            <Button class="flex flex-row text-nowrap"><PlusOutline class="w-6 h-8 my-auto"/></Button>
        </div>
    </div>
    
    <div class="flex flex-col grow min-h-0 bg-slate-300 overflow-y-scroll">
        <!-- COMPONENT: ActionRepositoryListItem -->
        <div class="flex flex-col px-2 my-1 border-t-2 border-black hover:bg-slate-400">
            <div class="font-bold">
                Home assistant actions
            </div>
            <div>
                URL: http://golem:8125/PistaMista/HA-actions.git
            </div>
        </div>
    </div>
</div>