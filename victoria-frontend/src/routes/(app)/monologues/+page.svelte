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
                <Button class="flex flex-row">Trigger<ChevronDownOutline class="w-6 h-6"/></Button>
                <Dropdown>
                    <DropdownItem>Timer</DropdownItem>
                    <DropdownItem>Chat Message</DropdownItem>
                    <DropdownItem>Webhook</DropdownItem>
                    <DropdownItem>Monologue success</DropdownItem>
                </Dropdown>
            </div>
            <div class="hover:bg-slate-300 p-1 rounded-md">
                <Button class="flex flex-row">Status<ChevronDownOutline class="w-6 h-6"/></Button>
                <Dropdown>
                    <DropdownItem>PENDING</DropdownItem>
                    <DropdownItem>RUNNING</DropdownItem>
                    <DropdownItem>SUCCESS</DropdownItem>
                    <DropdownItem>FAILURE</DropdownItem>
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
        <div class="flex flex-row px-2 my-1 border-t-2 border-black hover:bg-slate-400">
            <div class="content-center">
                <div class="flex flex-col">
                    <!-- This is a MonologueStatusIndicator -->
                    <div class="font-bold text-lime-600 rounded-md bg-slate-600 p-1">
                        RUNNING
                    </div>
                    <div class="text-center">
                        20m39s
                    </div>
                </div>
            </div>
            <div class="grow mx-2 min-w-0 flex flex-col">
                <div class="font-bold">
                    Research thesis ideas
                </div>
                <div>
                    Searching the web for sources...
                </div>

                <div>
                    Started by <span class="font-semibold text-blue-500">Researcher</span> (<span class="font-semibold text-orange-400">Timer</span>) 20m ago
                </div>
            </div>
        </div>
    </div>
</div>