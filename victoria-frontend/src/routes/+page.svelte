<script lang="ts">
    import PromptBox from '$lib/PromptBox.svelte';
    import ChatWindow from '$lib/ChatWindow.svelte';
    import ErrorAlert from '$lib/ErrorAlert.svelte';

    let prompt = "";
    let messages: Array<any> = [ ];
    let processing = false;
    let error: any = null;
    
    async function on_submit() {
        if (processing) {
            return
        }

        messages = [...messages, {type: 'user', content: prompt}];
        prompt = "";
        
        processing = true;

        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: new Headers({'content-type': 'application/json'}),
            body: JSON.stringify({
                messages: messages
            })
        });
        
        if (response.ok) {
            const json = await response.json();
            messages = [...messages, json]
            error = null;
        } else {
            error = {
                status: response.status,
                statusText: response.statusText
            }
        }
        
        processing = false;
    }
</script>

<div class="flex flex-col absolute inset-0">
    {#if error}
        <ErrorAlert>
            <span slot="status"> {error.status} </span>
            <span slot="statusText"> {error.statusText} </span>
        </ErrorAlert>
    {/if} 

    <div class="grow overflow-hidden">
        <ChatWindow {messages}/>
    </div>
    
    <div>
        <PromptBox bind:prompt {on_submit} show_spinner={processing} autofocus/>
    </div>
</div>