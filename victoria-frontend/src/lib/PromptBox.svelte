<script>
    import { Input, Button, ButtonGroup, Spinner, Textarea } from 'flowbite-svelte';
    import { PaperPlaneOutline } from 'flowbite-svelte-icons';
    
    export let prompt = "";
    export let autofocus = false;
    export let show_spinner = false;
    export let on_submit = () => {};
</script>

<div class="m-2 p-2 max-h-1/6">
    <form on:submit={() => { if (!show_spinner) { on_submit() }}}>
        <ButtonGroup class="w-full">
            <Textarea 
                placeholder="Type..."
                class="rounded-r-none"
                bind:value={prompt}
                {autofocus}
            />
            <Button color="primary" disabled={prompt.length == 0 || show_spinner} type="submit">
                {#if show_spinner}
                    <Spinner size="4"/>
                {:else}
                    <PaperPlaneOutline/>
                {/if}
            </Button>
        </ButtonGroup>
    </form>
</div>