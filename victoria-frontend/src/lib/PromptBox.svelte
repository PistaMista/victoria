<script>
    import { Input, Button, ButtonGroup, Spinner } from 'flowbite-svelte';
    import { PaperPlaneOutline } from 'flowbite-svelte-icons';
    
    export let prompt = "";
    export let autofocus = false;
    export let show_spinner = false;
    export let on_submit = () => {};
</script>

<div class="m-2 p-2">
    <form on:submit={() => { if (!show_spinner) { on_submit() }}}>
        <ButtonGroup class="w-full">
            {#if autofocus}
                <Input 
                    placeholder="Type..." 
                    type="text" 
                    bind:value={prompt} 
                    autofocus
                />
            {:else}
                <Input 
                    placeholder="Type..." 
                    type="text" 
                    bind:value={prompt} 
                />
            {/if}
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