<script lang="ts">
    import { afterUpdate } from "svelte";
    import AssistantMessage from "./ChatItem/AssistantMessage.svelte";
    import UserMessage from "./ChatItem/UserMessage.svelte";
    
    export let messages: Array<any> = [];
    
    let container: HTMLDivElement;

    // Scroll to the last message when the container element changes
    afterUpdate(() => {
        container.scrollTo(0, container.scrollHeight);
    })
</script>

<div class="p-2 w-full h-full">
    <div class="p-2 h-full bg-gray-200 border border-slate-600 focus:border-primary-900 shadow-inner rounded-lg">
        <div bind:this={container} class="p-2 h-full overflow-y-auto scroll-smooth">
            {#each messages as message}
                {#if message.type == 'user'}
                    <UserMessage> {message.content} </UserMessage>
                {:else}
                    <AssistantMessage content={message.content}/>
                {/if}
            {/each}
        </div>
    </div>
</div>