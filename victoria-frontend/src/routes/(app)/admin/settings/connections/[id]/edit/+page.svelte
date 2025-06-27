<script>
    import { Label, Button, Input } from "flowbite-svelte";
    import {  ChevronLeftOutline, PlusOutline, TrashBinSolid, CogSolid } from "flowbite-svelte-icons";
</script>

<!-- COMPONENT: ConnectionDetailView -->
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
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">URL</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <Input/>
            </div>
        </div>

        <div class="my-2">
            <!-- COMPONENT: DetailViewSection -->
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">API Key</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <Input/>
            </div>
        </div>

        <!-- COMPONENT: DeleteButton -->
        <Button class="font-bold bg-red-500">
            DELETE CONNECTION
        </Button>
        
        <!-- COMPONENT: SaveButton -->
        <Button class="font-bold bg-lime-500">
            ADD CONNECTION
        </Button>
    </div>
</div>