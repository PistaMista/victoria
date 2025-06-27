<script>
    import { Label, Button, Input, Dropdown, DropdownItem, Textarea } from "flowbite-svelte";
    import { LinkOutline, CogSolid, BrainSolid, ChevronRightOutline, ChevronLeftOutline, ChevronDownOutline } from "flowbite-svelte-icons";
</script>

<!-- COMPONENT: TriggerDetailView -->
<!-- COMPONENT: DetailView -->
<div class="w-full h-full overflow-y-auto">
    <div class="hidden md:inline float-left">
        <!-- COMPONENT: BackButton -->
        <div class="flex flex-row hover:bg-slate-500 rounded-md p-1">
            <ChevronLeftOutline class="h-8 w-8 my-auto"/>
            <div class="content-center mr-2">
                Back
            </div>
        </div>
    </div>

    <div class="flex flex-col content-center mx-2 md:m-auto md:max-w-96">
        <div class="md:hidden">
            <!-- COMPONENT: BackButton -->
            <div class="flex flex-row hover:bg-slate-500 rounded-md p-1">
                <ChevronLeftOutline class="h-8 w-8 my-auto"/>
                <div class="content-center mr-2">
                    Back
                </div>
            </div>
        </div>            
        
        <div class="my-2">
            <!-- COMPONENT: DetailViewSection -->
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Trigger</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <div class="flex flex-col space-y-2">
                    <div>
                        <!-- COMPONENT: LabeledSetting -->
                        <Label>Name</Label>                        
                        <Input/>
                    </div>

                    <div>
                        <!-- COMPONENT: LabeledSetting -->
                        <Label>Type</Label>
                        <!-- COMPONENT: TriggerTypeDropdown -->
                        <Button class="flex flex-row w-full">WEBHOOK<ChevronDownOutline class="w-6 h-6"/></Button>
                        <Dropdown>
                            <DropdownItem>Timer</DropdownItem>
                            <DropdownItem>Chat Message</DropdownItem>
                            <DropdownItem>Webhook</DropdownItem>
                            <DropdownItem>Poll</DropdownItem>
                        </Dropdown>
                    </div>
                    
                    <!-- These are type-specific -->
                    <!-- COMPONENT: PollTriggerSettings -->
                    <div>
                        <!-- Poll settings -->
                        <!-- COMPONENT: LabeledSetting -->
                        <Label>Polled URL</Label>
                        <Input/>
                    </div>

                    <!-- These are type-specific -->
                    <!-- COMPONENT: ChatTriggerSettings -->
                    <div>
                        <!-- Chat settings -->
                        <!-- COMPONENT: LabeledSetting -->
                        <Label>Chat receiver name</Label>
                        <Input/>
                    </div>

                    <!-- These are type-specific -->
                    <!-- COMPONENT: ChatTriggerSettings -->
                    <div>
                        <!-- Webhook settings -->
                        <!-- COMPONENT: LabeledSetting -->
                        <Label>Relative webhook URL</Label>
                        <Input/>
                    </div>

                    <!-- COMPONENT: TimerTriggerSettings -->
                    <div>
                        <!-- Timer settings TODO -->
                    </div>
                </div>
            </div>
        </div>

        <div class="my-2">
            <!-- COMPONENT: DetailViewSection -->
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Parser</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <div class="flex flex-col space-y-2">
                    <div>
                        <!-- COMPONENT: LabeledSetting -->
                        <Label>Type</Label>
                        <!-- COMPONENT: ParserTypeDropdown -->
                        <Button class="flex flex-row w-full">IDENTITY<ChevronDownOutline class="w-6 h-6"/></Button>
                        <Dropdown>
                            <DropdownItem>Identity</DropdownItem>
                            <DropdownItem>JSON</DropdownItem>
                            <DropdownItem>XML</DropdownItem>
                        </Dropdown>
                    </div>

                    <div>
                        <!-- COMPONENT: LabeledSetting -->
                        <Label>Settings</Label>                        
                        
                        <div>SOME SETTINGS TO CHANGE</div>
                    </div>

                </div>
            </div>
        </div>

        <div class="my-2">
            <!-- COMPONENT: DetailViewSection -->
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Template</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <!-- COMPONENT: EventTemplateEditor -->
                <!-- COMPONENT: LabeledSetting -->
                <Label>Parser variables</Label>
                <div class="flex flex-row flex-wrap rounded-md bg-black">
                    <!-- COMPONENT: ParserVariableListItem -->
                    <div class="m-0.5 font-bold text-orange-500">
                        $content
                    </div>

                    <!-- COMPONENT: ParserVariableListItem -->
                    <div class="m-0.5 font-bold text-orange-500">
                        $key
                    </div>
                </div>
                
                <!-- COMPONENT: LabeledSetting -->
                <Label>Event template</Label>
                <!-- COMPONENT: EventTemplateEditor -->
                <Textarea/>
            </div>
        </div>
        
        <!-- COMPONENT: DeleteButton -->
        <Button class="w-full bg-red-500">Delete trigger</Button>

        <!-- COMPONENT: SaveButton -->
        <div class="my-3">
            <Button class="w-full">Save trigger</Button>
        </div>
    </div>
</div>