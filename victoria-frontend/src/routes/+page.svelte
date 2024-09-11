<script lang="ts">
    import PromptBox from '$lib/PromptBox.svelte';
    import ChatWindow from '$lib/ChatWindow.svelte';

    let prompt = "";
    let messages: Array<any> = [
        {type: 'user'},
        {type: 'assistant'},
        {type: 'user'},
        {type: 'user'},
        {type: 'assistant'},
        {type: 'assistant'},
        {type: 'assistant'},
        {type: 'user'},
        {type: 'assistant'},
        {type: 'user'},
        {type: 'user'},
        {type: 'assistant'},
        {type: 'assistant'},
        {type: 'assistant'},
        {type: 'user'},
        {type: 'assistant'},
        {type: 'user'},
        {type: 'user'},
        {type: 'assistant'},
        {type: 'assistant'},
        {type: 'assistant'},
        {type: 'user'},
        {type: 'user'},
        {type: 'user'},
        {type: 'user'},
        {type: 'user'},
        {type: 'user'},
    ];
    
    function on_submit() {
        console.log(`Submitted prompt: "${prompt}"`);
        prompt = "";
    }
</script>


<div class="flex flex-col absolute inset-0">
    <div class="grow overflow-hidden">
        <ChatWindow {messages}/>
    </div>
    <PromptBox bind:prompt {on_submit} autofocus/>
</div>
