<script lang="ts">
    import {  Button, Range, Input, Label, Toggle } from "flowbite-svelte";
    import { RefreshOutline } from "flowbite-svelte-icons";
</script>

<div class="w-full h-full overflow-y-auto">
    <div class="flex flex-col content-center mx-2 md:m-auto md:max-w-96">
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
        <div class="my-2">
            <!-- This is a DetailViewSection -->
            <!-- This section is the same as the Agent Detail's Model parameters section -->
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Model parameters</Label>
            <div class="bg-slate-400 rounded-md p-2">
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
    </div>
</div>