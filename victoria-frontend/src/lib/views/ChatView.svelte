<script lang="ts">
    import ChatWindow from "$lib/components/chat/ChatWindow.svelte";
    import ChatPrompt from "$lib/components/chat/ChatPrompt.svelte";
    
    export let id: number;
</script>

<div class="w-full h-full flex flex-col pt-2 md:pb-2">
    <ChatWindow {id}/>
    <ChatPrompt {id}/>
</div>