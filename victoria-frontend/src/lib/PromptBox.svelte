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
            <Button color="primary" disabled={prompt.length == 0} type="submit">
                <PaperPlaneOutline/>
            </Button>
        </ButtonGroup>
    </form>
</div>