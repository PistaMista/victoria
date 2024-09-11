<script lang="ts">
    import AssistantMessage from "./ChatItem/AssistantMessage.svelte";
    import UserMessage from "./ChatItem/UserMessage.svelte";
    
    export let messages: Array<any> = [];
</script>

<div class="p-2 w-full h-full">
    <div class="p-2 h-full bg-gray-200 border border-slate-600 focus:border-primary-900 shadow-inner rounded-lg">
        <div class="p-2 h-full overflow-y-auto">
            {#each messages as message}
                {#if message.type == 'user'}
                    <UserMessage> {message.content} </UserMessage>
                {:else}
                    <AssistantMessage> {message.content} </AssistantMessage>
                {/if}
            {/each}
        </div>
    </div>
</div>