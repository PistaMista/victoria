<script>
    import { Label, Range, Input, Button } from "flowbite-svelte";
    import { RefreshOutline } from "flowbite-svelte-icons";
</script>

<div class="flex flex-row mt-2">
    <div class="grow flex flex-col">
        <Label>Temperature</Label>
        <Range class="place-self-center ml-1 grow"/>
    </div>
    <Input value={20} class="place-self-center ml-1 w-12"/>
    <Button class="p-1 ml-1"><RefreshOutline></RefreshOutline></Button>
</div>