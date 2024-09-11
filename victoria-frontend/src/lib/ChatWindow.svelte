<script lang="ts">
    import AssistantMessage from "./ChatItem/AssistantMessage.svelte";
    import UserMessage from "./ChatItem/UserMessage.svelte";
    
    export let messages: Array<any> = [];
</script>

<div class="p-2 w-full h-full">
    <div 
        class="
            p-2 w-full h-full 
            overflow-y-scroll 
            bg-gray-200 border border-slate-600 
            focus:border-primary-900
            shadow-inner rounded-lg"
    >
        {#each messages as message}
            {#if message.type == 'user'}
                <UserMessage/>
            {:else}
                <AssistantMessage/>
            {/if}
        {/each}
    </div>
</div>