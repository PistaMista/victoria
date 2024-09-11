<script>
    import { Input, Button, ButtonGroup } from 'flowbite-svelte';
    import { PaperPlaneOutline } from 'flowbite-svelte-icons';
    
    export let prompt = "";
    export let autofocus = false;
    export let on_submit = () => {};
</script>

<div class="m-2 p-2">
    <form on:submit={on_submit}>
        <ButtonGroup class="w-full">
            <Input placeholder="Type..." type="text" bind:value={prompt} {autofocus}/>
            <Button color="primary" disabled={prompt.length == 0} type="submit">
                <PaperPlaneOutline/>
            </Button>
        </ButtonGroup>
    </form>
</div>