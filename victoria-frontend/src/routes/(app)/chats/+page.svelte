<script lang="ts">
    import Button from "$lib/components/button/Button.svelte";
    import { Search, Dropdown, DropdownItem } from "flowbite-svelte";   
    import { ChevronDoubleDownOutline, ChevronDownOutline, PlusOutline } from "flowbite-svelte-icons";
</script>

<!-- COMPONENT: ChatListView -->
<!-- COMPONENT: ListView -->
<div class="flex flex-col w-full h-full">
    <div class="p-1 bg-slate-400 flex flex-col md:flex-row">
        <!-- COMPONENT: ListViewHeaderSearchBar -->
        <Search class="grow max-h-8 md:max-w-72 mb-1 md:mb-0"></Search>
        
        <div class="mx-2 content-center flex flex-row">
            <!-- COMPONENT: ListViewHeaderDropdown -->
            <div class="hover:bg-slate-300 p-1 rounded-md">
                <Button class="flex flex-row">Sort<ChevronDownOutline class="w-6 h-6"/></Button>
                <Dropdown>
                    <DropdownItem>Recent</DropdownItem>
                    <DropdownItem>Longest</DropdownItem>
                    <DropdownItem>Importance</DropdownItem>
                </Dropdown>
            </div>
            <!-- COMPONENT: ListViewHeaderDropdown -->
            <div class="hover:bg-slate-300 p-1 rounded-md">
                <Button class="flex flex-row">Agent<ChevronDownOutline class="w-6 h-6"/></Button>
                <Dropdown>
                    <DropdownItem>Cook</DropdownItem>
                    <DropdownItem>Researcher</DropdownItem>
                </Dropdown>
            </div>
            <!-- COMPONENT: ListViewHeaderButton -->
            <div class="hover:bg-slate-300 p-1 rounded-md">
                <Button class="flex flex-row text-nowrap"><PlusOutline class="w-6 h-6"/></Button>
            </div>
        </div>
    </div>
    
    <div class="flex flex-col grow min-h-0 bg-slate-300 overflow-y-scroll">
        <!-- COMPONENT: ChatListItem (styling left to ListView) -->
        <div class="flex flex-col px-2 my-1 border-t-2 border-black hover:bg-slate-400">
            <div class="font-bold">System administration</div>
            <div>Discusses various system administration activities.</div>
        </div>
    </div>
</div>