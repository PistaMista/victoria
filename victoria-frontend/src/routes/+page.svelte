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
            body: JSON.stringify({})
        });
        
        if (response.ok) {
            const json = await response.json();
            messages = [...messages, {type: 'assistant', content: json.body}]
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
            <div slot="status"> {error.status} </div>
            <div slot="statusText"> {error.statusText} </div>
        </ErrorAlert>
    {/if} 

    <div class="grow overflow-hidden">
        <ChatWindow {messages}/>
    </div>
    
    <div>
        <PromptBox bind:prompt {on_submit} show_spinner={processing} autofocus/>
    </div>
</div>