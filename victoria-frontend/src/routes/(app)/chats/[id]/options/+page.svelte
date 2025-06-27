<script lang="ts">
    import {  Button, Range, Input, Label, Checkbox, Dropdown, DropdownItem } from "flowbite-svelte";
    import { ChevronDownOutline } from "flowbite-svelte-icons";
</script>

<!-- COMPONENT: ChatOptionsView -->
<!-- COMPONENT: DetailView -->
<div class="w-full h-full overflow-y-auto">
    <div class="flex flex-col content-center mx-2 md:m-auto md:max-w-96">
        <div class="my-2">
            <!-- COMPONENT: DetailViewSection -->
            <!-- This section is the same as the Agent Detail's Actions section -->
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Message recipient</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <!-- COMPONENT: ChatReceiverDropdown -->
                <Button class="flex flex-row w-full">General<ChevronDownOutline class="w-6 h-6"/></Button>
                <Dropdown>
                    <DropdownItem>General</DropdownItem>
                    <DropdownItem>Technical</DropdownItem>
                    <DropdownItem>Research</DropdownItem>
                </Dropdown>
            </div>
        </div>
        <div class="my-2">
            <!-- COMPONENT: DetailViewSection -->
            <!-- This section is the same as the Agent Detail's Actions section -->
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Allowed actions</Label>
            <div class="bg-slate-400 rounded-md p-2">
                    <!-- COMPONENT: ActionToggle -->
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Send chat message
                        </div>
                        <Checkbox/>
                    </div>
                    <!-- COMPONENT: ActionToggle -->
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Search web
                        </div>
                        <Checkbox/>
                    </div>
                    <!-- COMPONENT: ActionToggle -->
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Access task list
                        </div>
                        <Checkbox/>
                    </div>
                    <!-- COMPONENT: ActionToggle -->
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Access Zettelkasten
                        </div>
                        <Checkbox/>
                    </div>
                    <!-- COMPONENT: ActionToggle -->
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Use memory
                        </div>
                        <Checkbox/>
                    </div>
            </div>
        </div>

        <!-- COMPONENT: DeleteButton -->
        <div class="my-3">
            <Button class="w-full bg-red-500">Delete chat</Button>
        </div>

        <!-- COMPONENT: SaveButton -->
        <div class="my-3">
            <Button class="w-full">Save options</Button>
        </div>
    </div>
</div>