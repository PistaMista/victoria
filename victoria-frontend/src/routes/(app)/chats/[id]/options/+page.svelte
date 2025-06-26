<script lang="ts">
    import {  Button, Range, Input, Label, Toggle, Dropdown, DropdownItem } from "flowbite-svelte";
    import { ChevronDownOutline } from "flowbite-svelte-icons";
</script>

<div class="w-full h-full overflow-y-auto">
    <div class="flex flex-col content-center mx-2 md:m-auto md:max-w-96">
        <div class="my-2">
            <!-- This is a DetailViewSection -->
            <!-- This section is the same as the Agent Detail's Actions section -->
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Message recipient</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <Button class="flex flex-row w-full">General<ChevronDownOutline class="w-6 h-6"/></Button>
                <Dropdown>
                    <DropdownItem>General</DropdownItem>
                    <DropdownItem>Technical</DropdownItem>
                    <DropdownItem>Research</DropdownItem>
                </Dropdown>
            </div>
        </div>
        <div class="my-2">
            <!-- This is a DetailViewSection -->
            <!-- This section is the same as the Agent Detail's Actions section -->
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Allowed actions</Label>
            <div class="bg-slate-400 rounded-md p-2">
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Send chat message
                        </div>
                        <Toggle/>
                    </div>
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Search web
                        </div>
                        <Toggle/>
                    </div>
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Access task list
                        </div>
                        <Toggle/>
                    </div>
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Access Zettelkasten
                        </div>
                        <Toggle/>
                    </div>
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Use memory
                        </div>
                        <Toggle/>
                    </div>
            </div>
        </div>
    </div>
</div>