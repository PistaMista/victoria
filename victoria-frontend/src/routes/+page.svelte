<script lang="ts">
    import PromptBox from '$lib/PromptBox.svelte';
    import ChatWindow from '$lib/ChatWindow.svelte';

    let prompt = "";
    let messages: Array<any> = [ ];
    let processing = false;
    
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
        
        const json = await response.json();
        messages = [...messages, {type: 'assistant', content: json.body}]
        
        processing = false;
    }
</script>


<div class="flex flex-col absolute inset-0">
    <div class="grow overflow-hidden">
        <ChatWindow {messages}/>
    </div>
    
    <div>
        <PromptBox bind:prompt {on_submit} show_spinner={processing} autofocus/>
    </div>
</div>
