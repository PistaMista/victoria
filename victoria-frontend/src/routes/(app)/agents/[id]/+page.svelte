<script lang="ts">
    import { Textarea, Button, Range, Input, Label, Dropdown, DropdownItem, Checkbox } from "flowbite-svelte";
    import { RefreshOutline, ChevronDownOutline } from "flowbite-svelte-icons";
</script>

<div class="w-full h-full overflow-y-auto">
    <div class="flex flex-row">
        <div class="md:basis-1/5"/>
        <div class="grow md:basis-3/5 flex flex-col p-2">
            <div class="font-bold">
                Researcher
            </div>
            <!-- This is a DetailViewSection -->
            <div class="my-2">
                <Label class="sticky top-0 bg-white px-2 font-bold">Thumbnail</Label>
                <div class="bg-slate-400 rounded-md p-2">
                    <div class="place-self-center">
                        <div class="w-48 h-48 bg-yellow-200 rounded-md"></div>
                        <Button class="m-2">Pick image</Button>
                    </div>
                </div>
            </div>
            <div class="my-2">
                <Label class="sticky top-0 bg-white px-2 font-bold">Base model</Label>
                <div class="rounded-md bg-slate-400 p-2">
                    <Button class="flex flex-row w-full">gemma3:12b<ChevronDownOutline class="w-6 h-6"/></Button>
                    <Dropdown>
                        <DropdownItem>gemma3:12b</DropdownItem>
                        <DropdownItem>llama3.1:8b</DropdownItem>
                        <DropdownItem>qwen2.5:7b</DropdownItem>
                    </Dropdown>
                </div>
            </div>
            <div class="my-2">
                <Label class="sticky top-0 bg-white px-2 font-bold">System prompt</Label>
                <div class="rounded-md bg-slate-400 p-2">
                    <Textarea/>
                </div>
            </div>
            <div class="my-2">
                <!-- This section is the same as the chat options's Model parameters section -->
                <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Model parameters</Label>
                <div class="rounded-md bg-slate-400 p-2">
                    <div class="flex flex-row mt-2">
                        <div class="grow flex flex-col">
                            <Label>Temperature</Label>
                            <Range class="place-self-center ml-1 grow"/>
                        </div>
                        <Input value={20} class="place-self-center ml-1 w-12"/>
                        <Button class="p-1 ml-1"><RefreshOutline></RefreshOutline></Button>
                    </div>
                    <div class="flex flex-row mt-2">
                        <div class="grow flex flex-col">
                            <Label>Low-k</Label>
                            <Range class="place-self-center ml-1 grow"/>
                        </div>
                        <Input value={20} class="place-self-center ml-1 w-12"/>
                        <Button class="p-1 ml-1"><RefreshOutline></RefreshOutline></Button>
                    </div>
                    <div class="flex flex-row mt-2">
                        <div class="grow flex flex-col">
                            <Label>Tokens To Keep On Context Refresh</Label>
                            <Range class="place-self-center ml-1 grow"/>
                        </div>
                        <Input value={20} class="place-self-center ml-1 w-12"/>
                        <Button class="p-1 ml-1"><RefreshOutline></RefreshOutline></Button>
                    </div>

                </div>
            </div>
            <div class="my-2">
                <!-- This section is the same as the permitted triggers view for users -->
                <Label class="sticky top-0 bg-white px-2 z-40 font-bold"> Triggers </Label>
                <div class="bg-slate-400 rounded-md p-2">
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Chat
                        </div>
                        <Checkbox/>
                    </div>
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Timer
                        </div>
                        <Checkbox/>
                    </div>
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Task passing due date
                        </div>
                        <Checkbox/>
                    </div>
                </div>
            </div>
            <div class="my-2">
            <!-- This section is the same as the chat options view and permitted actions view for users -->
                <Label class="sticky top-0 bg-white px-2 z-40 font-bold"> Actions </Label>
                <div class="bg-slate-400 rounded-md p-2">
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Send chat message
                        </div>
                        <Checkbox/>
                    </div>
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Search web
                        </div>
                        <Checkbox/>
                    </div>
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Access task list
                        </div>
                        <Checkbox/>
                    </div>
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Access Zettelkasten
                        </div>
                        <Checkbox/>
                    </div>
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Use memory
                        </div>
                        <Checkbox/>
                    </div>
                </div>
            </div>
            <div class="my-3">
                <Button class="w-full bg-red-500">Delete agent</Button>
            </div>
            <div class="my-3">
                <Button class="w-full">Save agent</Button>
            </div>
        </div>
        <div class="md:basis-1/5"/>
    </div>
</div>