<script lang="ts">
    import PromptBox from '$lib/PromptBox.svelte';
    import ChatWindow from '$lib/ChatWindow.svelte';

    let prompt = "";
    
    function on_submit() {
        console.log(`Submitted prompt: "${prompt}"`);
        prompt = "";
    }
</script>


<div class="flex flex-col absolute inset-0">
    <div class="grow">
        <ChatWindow/>
    </div>
    <div class="justify-end">
        <PromptBox bind:prompt {on_submit} autofocus/>
    </div>
</div>
