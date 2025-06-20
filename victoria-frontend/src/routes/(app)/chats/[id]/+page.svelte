<script>
    import { ButtonGroup, Textarea, Button } from "flowbite-svelte";
    import { PaperPlaneSolid, PaperClipOutline, HammerSolid } from "flowbite-svelte-icons";
</script>

<div class="w-full h-full flex flex-col md:p-2">
    <div class="grow min-h-0 mb-2 overflow-y-scroll">
        <div class="flex flex-col md:w-2/3 mx-2 md:m-auto">
            <div class="w-full bg-red-400 rounded-md min-h-[1800px]"></div>
        </div>
    </div>
    <ButtonGroup class="md:bg-slate-400 p-0 md:p-2 md:w-2/3 md:m-auto rounded-none md:rounded-md">
        <Button class="w-8 min-h-0"><HammerSolid/></Button>
        <Button class="w-8 min-h-0"><PaperClipOutline/></Button>
        <Textarea class="bg-slate-200 border-none rounded-none"/>
        <Button class="w-12 min-h-0"><PaperPlaneSolid/></Button>
    </ButtonGroup>
</div>