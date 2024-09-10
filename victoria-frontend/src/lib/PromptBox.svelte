<script>
    import { Input, Button, ButtonGroup } from 'flowbite-svelte';
    import { PaperPlaneOutline } from 'flowbite-svelte-icons';
    
    export let prompt = "";
    export let on_submit = () => {};
</script>

<div class="m-2 p-2">
    <ButtonGroup class="w-full">
        <Input placeholder="Type..." bind:value={prompt} type="text"/>
        <Button color="primary" disabled={prompt.length == 0} on:click={on_submit}>
            <PaperPlaneOutline/>
        </Button>
    </ButtonGroup>
</div>