<script lang="ts">
    import { ButtonGroup, Button, Textarea } from "flowbite-svelte";
    import { PaperClipOutline, PaperPlaneSolid, HammerSolid } from "flowbite-svelte-icons";
</script>

<ButtonGroup class="md:bg-slate-400 p-0 md:p-2 md:w-2/3 md:m-auto rounded-none md:rounded-md">
    <Button class="w-8 min-h-0"><HammerSolid/></Button>
    <Button class="w-8 min-h-0"><PaperClipOutline/></Button>
    <Textarea class="bg-slate-200 border-none rounded-none"/>
    <Button class="w-12 min-h-0"><PaperPlaneSolid/></Button>
</ButtonGroup>