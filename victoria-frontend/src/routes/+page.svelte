<script lang="ts">
    import PromptBox from '$lib/PromptBox.svelte';
    import ChatWindow from '$lib/ChatWindow.svelte';

    let prompt = "";
    let messages: Array<any> = [ ];
    
    function on_submit() {
        messages = [...messages, {type: 'user', content: prompt}];
        prompt = "";
    }
</script>


<div class="flex flex-col absolute inset-0">
    <div class="grow overflow-hidden">
        <ChatWindow {messages}/>
    </div>
    <PromptBox bind:prompt {on_submit} autofocus/>
</div>
