<script>
    import { Label, Button, Input, Dropdown, DropdownItem, Textarea } from "flowbite-svelte";
    import { LinkOutline, CogSolid, BrainSolid, ChevronRightOutline, ChevronLeftOutline, ChevronDownOutline } from "flowbite-svelte-icons";
</script>

<!-- COMPONENT: ActionRepositoryDetailView -->
<!-- COMPONENT: DetailView -->
<div class="w-full h-full overflow-y-auto">
    <!-- FIXME: This back button should stay fixed it should not scroll -->
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
            <!-- COMPONENT:BackButton -->
            <div class="flex flex-row hover:bg-slate-500 rounded-md p-1">
                <ChevronLeftOutline class="h-8 w-8 my-auto"/>
                <div class="content-center mr-2">
                    Back
                </div>
            </div>
        </div>            
        
        <div class="my-2">
            <!-- COMPONENT: DetailViewSection -->
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Action repository</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <div class="flex flex-col space-y-2">
                    <!-- COMPONENT: LabeledSetting -->
                    <div>
                        <Label>Name</Label>                    
                        <Input/>
                    </div>
                    <!-- COMPONENT: LabeledSetting -->
                    <div>
                        <Label>URL</Label>                    
                        <Input/>
                    </div>
                </div>
            </div>
        </div>

        <!-- COMPONENT: SaveButton -->
        <div class="my-3">
            <Button class="w-full">Save action repository</Button>
        </div>
    </div>
</div>