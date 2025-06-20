<script lang="ts">
    import Button from "$lib/components/button/Button.svelte";
    import { Search, Dropdown, DropdownItem } from "flowbite-svelte";   
    import { ChevronDoubleDownOutline, ChevronDownOutline } from "flowbite-svelte-icons";
</script>

<div class="flex flex-col w-full h-full">
    <div class="p-1 bg-slate-400 flex flex-col md:flex-row">
        <Search class="grow max-h-8 md:max-w-72 mb-1 md:mb-0"></Search>
        <div class="mx-2 content-center flex flex-row">
            <div class="hover:bg-slate-300 p-1 rounded-md">
                <Button class="flex flex-row">Sort<ChevronDownOutline class="w-6 h-6"/></Button>
                <Dropdown>
                    <DropdownItem>Recent</DropdownItem>
                    <DropdownItem>Longest</DropdownItem>
                    <DropdownItem>Importance</DropdownItem>
                </Dropdown>
            </div>
            <div class="hover:bg-slate-300 p-1 rounded-md">
                <Button class="flex flex-row">Agent<ChevronDownOutline class="w-6 h-6"/></Button>
                <Dropdown>
                    <DropdownItem>Cook</DropdownItem>
                    <DropdownItem>Researcher</DropdownItem>
                </Dropdown>
            </div>
        </div>
    </div>
    
    <div class="flex flex-col grow min-h-0 bg-slate-300 overflow-y-scroll">
        <div class="flex flex-col px-2 my-1 border-t-2 border-black hover:bg-slate-400">
            <div class="font-bold">System administration</div>
            <div>Discusses various system administration activities.</div>
        </div>
    </div>
</div>